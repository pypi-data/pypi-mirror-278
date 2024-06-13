import os
from ipaddress import ip_address
from PySide2.QtWidgets import QLabel, QCheckBox, QRadioButton, QLineEdit, QPushButton
from PySide2.QtCore import QRegExp, QCoreApplication
from PySide2.QtGui import QIntValidator, QDoubleValidator, QRegExpValidator

from ..BaseUI import BaseUserInterface, MyQHBoxLayout, MyQVBoxLayout, MyQGroupBox
from pytessng.Config import PathConfig
from pytessng.GlobalVar import GlobalVar
from pytessng.ToolInterface import KafkaChecker


class SimuExportTrajectory(BaseUserInterface):
    name = "轨迹数据导出"

    # 记忆参数
    memory_params = {
        "is_coord": False,
        "is_json": False,
        "is_kafka": False,
        "coord_lon": None,
        "coord_lat": None,
        "json_path": PathConfig.DEFAULT_SAVE_TRAJ_DIR_PATH,
        "kafka_ip": None,
        "kafka_port": None,
        "kafka_topic": None
    }

    def __init__(self):
        super().__init__()
        # kafka有无问题
        self.kafka_is_ok = False

    # 设置界面布局
    def set_widget_layout(self):
        self.file_proj_string, file_proj_info = self.utils.read_file_proj()

        # 第一行：勾选框
        self.checkBox_coord = QCheckBox('写入经纬度坐标')
        # 第二行：单选框
        self.radio_proj_file = QRadioButton('使用路网创建时的投影')
        # 第三行：文本
        self.label_proj_file = QLabel(file_proj_info)
        # 第四行：单选框
        self.radio_proj_custom = QRadioButton('使用自定义高斯克吕格投影')
        # 第五行：文本和输入框，使用水平布局
        self.label_proj_custom_lon = QLabel('投影中心经度：')
        self.lineEdit_proj_custom_lon = QLineEdit()
        # 第六行：文本和输入框，使用水平布局
        self.label_proj_custom_lat = QLabel('投影中心纬度：')
        self.lineEdit_proj_custom_lat = QLineEdit()
        # 第七行：勾选框
        self.checkBox_json = QCheckBox('保存为Json文件')
        # 第八行：文本和按钮
        self.lineEdit_json = QLineEdit()
        self.lineEdit_json.setFixedWidth(500)
        self.button_json_save = QPushButton('选择保存位置')
        # 第九行：勾选框
        self.checkBox_kafka = QCheckBox('上传至kafka')
        # 第十行：文本和输入框
        self.label_kafka_ip = QLabel('IP：')
        self.lineEdit_kafka_ip = QLineEdit()
        self.label_kafka_port = QLabel('端口：')
        self.lineEdit_kafka_port = QLineEdit()
        # 第十一行：文本和输入框
        self.label_kafka_topic = QLabel('topic：')
        self.lineEdit_kafka_topic = QLineEdit()
        self.button_check_kafka = QPushButton('核验')
        self.label_check_info = QLabel('待核验')
        # 第十二行：按钮
        self.button = QPushButton('确定')

        # 总体布局
        layout = MyQVBoxLayout([
            self.checkBox_coord,
            MyQGroupBox(
                MyQVBoxLayout([
                    self.radio_proj_file,
                    self.label_proj_file,
                    self.radio_proj_custom,
                    MyQHBoxLayout([self.label_proj_custom_lon, self.lineEdit_proj_custom_lon]),
                    MyQHBoxLayout([self.label_proj_custom_lat, self.lineEdit_proj_custom_lat]),
                ])
            ),
            self.checkBox_json,
            MyQGroupBox(
                    MyQVBoxLayout([
                        MyQHBoxLayout([self.lineEdit_json, self.button_json_save])
                    ])
            ),
            self.checkBox_kafka,
            MyQGroupBox(
                MyQVBoxLayout([
                    MyQHBoxLayout([self.label_kafka_ip, self.lineEdit_kafka_ip, self.label_kafka_port, self.lineEdit_kafka_port]),
                    MyQHBoxLayout([self.label_kafka_topic, self.lineEdit_kafka_topic]),
                ])
            ),
            self.button
        ])
        self.setLayout(layout)

        # 限制输入框内容
        validator_coord = QDoubleValidator()
        self.lineEdit_proj_custom_lon.setValidator(validator_coord)
        self.lineEdit_proj_custom_lat.setValidator(validator_coord)
        validator_kafka_port = QIntValidator()
        self.lineEdit_kafka_port.setValidator(validator_kafka_port)
        regex = QRegExp("^[a-zA-Z][a-zA-Z0-9_]*$")
        validator_kafka_topic = QRegExpValidator(regex)
        self.lineEdit_kafka_topic.setValidator(validator_kafka_topic)

    def set_monitor_connect(self):
        self.checkBox_coord.stateChanged.connect(self.apply_monitor_state)
        self.radio_proj_custom.toggled.connect(self.apply_monitor_state)
        self.lineEdit_proj_custom_lon.textChanged.connect(self.apply_monitor_state)
        self.lineEdit_proj_custom_lat.textChanged.connect(self.apply_monitor_state)
        self.checkBox_json.stateChanged.connect(self.apply_monitor_state)
        self.lineEdit_json.textChanged.connect(self.apply_monitor_state)
        self.checkBox_kafka.stateChanged.connect(self.apply_monitor_state)
        self.lineEdit_kafka_ip.textChanged.connect(self.apply_monitor_state)
        self.lineEdit_kafka_port.textChanged.connect(self.apply_monitor_state)
        self.lineEdit_kafka_topic.textChanged.connect(self.apply_monitor_state)
        self.lineEdit_kafka_ip.textChanged.connect(self.apply_monitor_kafka)
        self.lineEdit_kafka_port.textChanged.connect(self.apply_monitor_kafka)

    def set_button_connect(self):
        self.button_json_save.clicked.connect(self.select_folder)
        self.button_check_kafka.clicked.connect(self.check_kafka)
        self.button.clicked.connect(self.apply_button_action)

    def set_default_state(self):
        if self.memory_params["is_coord"]:
            self.checkBox_coord.setChecked(True)
        if self.memory_params["is_json"]:
            self.checkBox_json.setChecked(True)
        if self.memory_params["is_kafka"]:
            self.checkBox_kafka.setChecked(True)
        if self.memory_params["coord_lon"] is not None:
            self.lineEdit_proj_custom_lon.setText(str(self.memory_params["coord_lon"]))
            self.lineEdit_proj_custom_lat.setText(str(self.memory_params["coord_lat"]))
        if self.memory_params["json_path"] is not None:
            self.lineEdit_json.setText(self.memory_params["json_path"])
        if self.memory_params["kafka_ip"] is not None:
            self.lineEdit_kafka_ip.setText(str(self.memory_params["kafka_ip"]))
            self.lineEdit_kafka_port.setText(str(self.memory_params["kafka_port"]))
            self.lineEdit_kafka_topic.setText(str(self.memory_params["kafka_topic"]))

        # 投影
        if bool(self.file_proj_string):
            self.radio_proj_file.setChecked(True)
        else:
            self.radio_proj_custom.setChecked(True)
        self.apply_monitor_state()

        # 创建默认保存文件夹
        if not os.path.exists(PathConfig.DEFAULT_SAVE_TRAJ_DIR_PATH):
            os.makedirs(PathConfig.DEFAULT_SAVE_TRAJ_DIR_PATH, exist_ok=True)

    def apply_monitor_state(self):
        # 勾选框的状态
        enabled_checkBox_coord = self.checkBox_coord.isChecked()
        # 文件投影的状态
        enabled_proj_file = bool(self.file_proj_string)
        # 选择投影方式的状态
        enabled_radio_proj = self.radio_proj_custom.isChecked()

        # 设置可用状态
        self.radio_proj_file.setEnabled(enabled_checkBox_coord and enabled_proj_file)
        self.label_proj_file.setEnabled(enabled_checkBox_coord and enabled_proj_file and not enabled_radio_proj)
        self.radio_proj_custom.setEnabled(enabled_checkBox_coord)
        self.label_proj_custom_lon.setEnabled(enabled_checkBox_coord and enabled_radio_proj)
        self.label_proj_custom_lat.setEnabled(enabled_checkBox_coord and enabled_radio_proj)
        self.lineEdit_proj_custom_lon.setEnabled(enabled_checkBox_coord and enabled_radio_proj)
        self.lineEdit_proj_custom_lat.setEnabled(enabled_checkBox_coord and enabled_radio_proj)

        ##############################

        # 勾选框的状态
        enabled_checkBox_json = self.checkBox_json.isChecked()

        # 设置可用状态
        self.lineEdit_json.setEnabled(enabled_checkBox_json)
        self.button_json_save.setEnabled(enabled_checkBox_json)

        ##############################

        # 勾选框的状态
        enabled_checkBox_kafka = self.checkBox_kafka.isChecked()

        # 设置可用状态
        self.label_kafka_ip.setEnabled(enabled_checkBox_kafka)
        self.lineEdit_kafka_ip.setEnabled(enabled_checkBox_kafka)
        self.label_kafka_port.setEnabled(enabled_checkBox_kafka)
        self.lineEdit_kafka_port.setEnabled(enabled_checkBox_kafka)
        self.label_kafka_topic.setEnabled(enabled_checkBox_kafka)
        self.lineEdit_kafka_topic.setEnabled(enabled_checkBox_kafka)
        self.button_check_kafka.setEnabled(enabled_checkBox_kafka)
        self.label_check_info.setEnabled(enabled_checkBox_kafka)

        ##############################

        # 设置按钮可用状态
        proj_state = False
        if not enabled_checkBox_coord:
            proj_state = True
        elif enabled_checkBox_coord and not enabled_radio_proj and enabled_proj_file:
            proj_state = True
        elif enabled_checkBox_coord and enabled_radio_proj:
            lon_0 = self.lineEdit_proj_custom_lon.text()
            lat_0 = self.lineEdit_proj_custom_lat.text()
            if lon_0 and lat_0 and -180 < float(lon_0) < 180 and -90 < float(lat_0) < 90:
                proj_state = True

        # Json有无问题
        folder_path = self.lineEdit_json.text()
        isdir = os.path.isdir(folder_path)
        json_state = (not enabled_checkBox_json) or (enabled_checkBox_json and isdir)
        if not (enabled_checkBox_json and isdir):
            GlobalVar.traj_json_config = None

        # Kafka有无问题
        kafka_state = (not enabled_checkBox_kafka) or (enabled_checkBox_kafka and self.kafka_is_ok)

        # 三个都没问题
        self.button.setEnabled(proj_state and json_state and kafka_state)

    # 特有方法：监测各组件状态，切换控件的可用状态
    def apply_monitor_kafka(self):
        self.kafka_is_ok = False
        self.label_check_info.setText("待核验")
        # 更新状态
        self.apply_monitor_state()

    def apply_button_action(self):
        # 获取投影
        if self.checkBox_coord.isChecked():
            self.memory_params["is_coord"] = True
            if self.radio_proj_custom.isChecked():
                lon_0 = float(self.lineEdit_proj_custom_lon.text())
                lat_0 = float(self.lineEdit_proj_custom_lat.text())
                self.memory_params["coord_lon"] = lon_0
                self.memory_params["coord_lat"] = lat_0
                traj_proj_string = f'+proj=tmerc +lon_0={lon_0} +lat_0={lat_0} +ellps=WGS84'
            else:
                traj_proj_string = self.file_proj_string
        else:
            self.memory_params["is_coord"] = False
            traj_proj_string = ""

        if self.checkBox_json.isChecked():
            self.memory_params["is_json"] = True
            traj_json_config = self.lineEdit_json.text()
            self.memory_params["json_path"] = traj_json_config
        else:
            self.memory_params["is_json"] = False
            traj_json_config = None

        if self.checkBox_kafka.isChecked() and self.kafka_is_ok:
            self.memory_params["is_kafka"] = True
            ip = self.lineEdit_kafka_ip.text()
            port = self.lineEdit_kafka_port.text()
            topic = self.lineEdit_kafka_topic.text()
            traj_kafka_config = {
                "ip": ip,
                "port": port,
                "topic": topic
            }
            self.memory_params["kafka_ip"] = ip
            self.memory_params["kafka_port"] = port
            self.memory_params["kafka_topic"] = topic
        else:
            self.memory_params["is_kafka"] = False
            traj_kafka_config = None

        # 配置全局变量
        GlobalVar.traj_proj_string = traj_proj_string
        GlobalVar.traj_json_config = traj_json_config
        GlobalVar.traj_kafka_config = traj_kafka_config

        # 关闭窗口
        self.close()

    # 特有方法：选择JSON保存文件夹
    def select_folder(self):
        folder_path = self.utils.open_folder()
        if folder_path:
            # 显示文件路径在LineEdit中
            self.lineEdit_json.setText(folder_path)

    # 特有方法：核验kafka
    def check_kafka(self):
        self.label_check_info.setText("核验中…")
        # 立刻更新界面
        QCoreApplication.processEvents()

        ip = self.lineEdit_kafka_ip.text()
        port = self.lineEdit_kafka_port.text()
        topic = self.lineEdit_kafka_topic.text()

        # 核验IP
        ip_is_ok = False
        if ip:
            try:
                ip_address(ip)
                ip_is_ok = True
            except:
                self.utils.show_info_box("请输入正确的IPv4地址", "warning")
                return
        else:
            self.utils.show_info_box("请输入IPv4地址", "warning")
            return
        # 核验端口
        port_is_ok = False
        if port:
            if int(port) > 0:
                port_is_ok = True
            else:
                self.utils.show_info_box("请输入大于0的端口号", "warning")
                return
        else:
            self.utils.show_info_box("请输入端口号", "warning")
            return
        # 核验topic
        topic_is_ok = False
        if topic:
            topic_is_ok = True
        else:
            self.utils.show_info_box("请输入topic", "warning")
            return

        kafka_pull_is_ok = KafkaChecker.check_kafka_pull(ip, port)

        # 如果都没问题
        if ip_is_ok and port_is_ok and topic_is_ok and kafka_pull_is_ok:
            self.kafka_is_ok = True
            self.label_check_info.setText("核验成功")
        else:
            self.kafka_is_ok = False
            self.label_check_info.setText("核验失败")

        # 更新状态
        self.apply_monitor_state()
