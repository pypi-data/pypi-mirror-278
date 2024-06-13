from abc import abstractmethod
from datetime import datetime

from ..BaseTool import BaseTool
from ..public.NetworkCreator import NetworkCreator


class BaseOther2Tessng(BaseTool):
    # 数据源
    data_source: str = ""
    # 进度条序号
    pgd_index_create_network = (1, 2)

    def __init__(self, netiface, auto_move: bool = False):
        super().__init__(netiface)
        # 是否自动移动到画布中心
        self.auto_move: bool = auto_move

        # 投影字符串
        self.proj_string: str = ""
        # move
        self.move_distance: dict = {"x_move": 0, "y_move": 0}

    def load_data(self, params: dict) -> dict:
        # 读取数据
        original_network_data = self.read_data(params)
        # 解析数据
        analyzed_network_data = self.analyze_data(original_network_data, params)
        # 创建路网
        response = self.create_network(analyzed_network_data)
        return response

    @abstractmethod
    def read_data(self, params: dict):
        pass

    @abstractmethod
    def analyze_data(self, original_network_data, params: dict) -> dict:
        pass

    def create_network(self, analyzed_network_data: dict) -> dict:
        links = analyzed_network_data["links"]
        # 如果有路段数据
        if links:
            # 计算move
            xs, ys = [], []
            for link in links:
                points = link["points"]
                xs.extend([point[0] for point in points])
                ys.extend([point[1] for point in points])
            x_center, y_center = [(min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2] if xs and ys else [0, 0]
            self.move_distance = {
                "x_move": -float(round(x_center, 3)),
                "y_move": -float(round(y_center, 3)),
            }
            move = self.move_distance if self.auto_move else None

            # 构建路网属性
            attrs = dict(
                data_source=self.data_source,
                created_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                proj_string=self.proj_string,
                move_distance=self.move_distance,
            )
            # 实例化路网创建者
            network_creator = NetworkCreator(
                self.netiface,
                move=move,
                pgd_index=self.pgd_index_create_network
            )
            # 设置路网属性
            network_creator.set_attrs(self.data_source, attrs)
            # 创建路网
            network_creator.create_network(analyzed_network_data)

            status = True,
            message = "创建成功"

        # 如果没路段数据
        else:
            status = False
            message = "所选文件中无数据或无合法数据"

        return {
            "status": status,
            "message": message,
        }
