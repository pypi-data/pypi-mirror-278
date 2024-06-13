import os
import time
import json
from datetime import datetime
from queue import Queue
from threading import Thread
from pyproj import Proj

from .TrajDataCalculator import TrajDataCalculator
from .KafkaMessage import KafkaMessageProducer
from pytessng.GlobalVar import GlobalVar
from pytessng.Logger import logger


class SimuExportTrajectoryActor:
    def __init__(self):
        self.json_save_path = None  # str
        self.kafka_producer = None  # KafkaMessageProducer

        # 比例尺转换
        self.p2m = None  # p2m (function)
        # 投影
        self.proj = None  # Proj (function)
        # move
        self.move = None  # dict

        # 运行状态
        self.is_running = False

        # 轨迹数据队列
        self.traj_data_queue = Queue()
        # 发送轨迹数据线程
        self.send_data_thread = None

    def ready(self, netiface):
        # =============== Json ===============
        traj_config_json: str = GlobalVar.simu_export_traj_config_json
        if traj_config_json:
            # 获取文件夹名称
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            folder_path = os.path.join(traj_config_json, f"轨迹数据_{current_time}")
            # 创建文件夹
            os.makedirs(folder_path, exist_ok=True)
            self.json_save_path = os.path.join(folder_path, "{}.json")

        # =============== Kakfa ===============
        traj_config_kafka: dict = GlobalVar.simu_export_traj_config_kafka
        if traj_config_kafka:
            ip = traj_config_kafka["ip"]
            port = traj_config_kafka["port"]
            topic = traj_config_kafka["topic"]
            self.kafka_producer = KafkaMessageProducer(f"{ip}:{port}", topic)

        # =============== 数据发送线程 ===============
        if traj_config_json or traj_config_kafka:
            # 比例尺转换
            scene_scale = netiface.sceneScale()
            self.p2m = lambda x: x * scene_scale

            # 投影关系
            traj_proj_string = GlobalVar.simu_export_traj_proj_string
            if traj_proj_string:
                self.proj = Proj(traj_proj_string)
            else:
                self.proj = lambda x, y, inverse=None: (None, None)

            # move
            move = netiface.netAttrs().otherAttrs().get("move_distance")
            if move is None or "tmerc" in traj_proj_string:
                self.move = {"x_move": 0, "y_move": 0}
            else:
                self.move = {"x_move": -move["x_move"], "y_move": -move["y_move"]}

            # 数据发送线程
            self.is_running = True
            self.send_data_thread = Thread(target=self.apply_send_data)
            self.send_data_thread.start()

    def finish(self):
        self.is_running = False

        # 清空队列
        while not self.traj_data_queue.empty():
            time.sleep(0.01)

        self.send_data_thread = None

        self.p2m = None  # p2m (function)
        self.proj = None  # Proj (function)
        self.move = None  # dict

        self.json_save_path = None  # str
        self.kafka_producer = None  # KafkaMessageProducer

    def send(self, simuiface: object):
        if self.is_running:
            # 计算轨迹数据
            traj_data = TrajDataCalculator.get_basic_traj_data(simuiface, self.p2m)
            # 放入队列
            self.traj_data_queue.put(traj_data)

    def apply_send_data(self):
        logger.logger_pytessng.info("The trajectory data sending thread has started.")

        while True:
            time.sleep(0.01)
            if self.traj_data_queue.empty():
                if self.is_running:
                    continue
                else:
                    logger.logger_pytessng.info("The trajectory data sending thread has been closed.")
                    break

            traj_data = self.traj_data_queue.get()  # 使用堵塞模式
            TrajDataCalculator.get_complete_traj_data(traj_data, self.proj, self.move)

            # 当前仿真计算批次
            batchNum = traj_data["batchNum"]

            t1 = time.time()
            # 需要保存为json
            if self.json_save_path:
                # 当前仿真计算批次
                file_path = self.json_save_path.format(batchNum)
                # 将JSON数据写入文件
                with open(file_path, 'w', encoding="utf-8") as file:
                    json.dump(traj_data, file, indent=4, ensure_ascii=False)

            t2 = time.time()
            # 需要上传至kafka
            if self.kafka_producer:
                traj_data_json = json.dumps(traj_data)
                self.is_running = self.kafka_producer.send_message(traj_data_json)
                if not self.is_running:
                    logger.logger_pytessng.info("Due to Kafka data sending failure, the trajectory data sending thread is closed.")
                    break

            t3 = time.time()
            json_time = round((t2 - t1) * 1000, 1)
            kafka_time = round((t3 - t2) * 1000, 1)

            logger.logger_pytessng.info(f"仿真批次：{batchNum}，导出时间：{json_time}ms，上传时间：{kafka_time}ms，队列大小：{self.traj_data_queue.qsize()}")
