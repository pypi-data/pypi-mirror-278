import os
from PySide2.QtWidgets import QLineEdit, QPushButton, QLabel, QCheckBox

from .BaseNetworkImport import BaseNetworkImport, MyQHBoxLayout, MyQVBoxLayout
from ..Utils import Utils
from pytessng.Config import PathConfig
from pytessng.ToolInterface import MyOperation


class NetworkImportOpenstreetmap(BaseNetworkImport):
    name: str = "导入OpenStreetMap"
    mode: str = "osm"
    format: list = [("OpenStreetMap", "osm")]

    def set_widget_layout(self):
        # 第一行：文本框和按钮
        self.line_edit = QLineEdit()
        self.line_edit.setFixedWidth(500)
        self.button_select = QPushButton('文件选择')
        # 第二行：勾选框
        self.label_select_roadType = QLabel("导入道路类型：")
        self.checkBoxes = [
            QCheckBox('高速公路'),
            QCheckBox('主干道路'),
            QCheckBox('低等级道路'),
        ]
        # 第三行：按钮
        self.button_import = QPushButton('生成路网文件')

        # 总体布局
        layout = MyQVBoxLayout([
            MyQHBoxLayout([self.line_edit, self.button_select]),
            MyQHBoxLayout([self.label_select_roadType] + self.checkBoxes),
            self.button_import,
        ])
        self.setLayout(layout)

    def set_monitor_connect(self):
        self.line_edit.textChanged.connect(self.apply_monitor_state)
        self.checkBoxes[1].stateChanged.connect(self.apply_monitor_state_checkBox_1)
        self.checkBoxes[2].stateChanged.connect(self.apply_monitor_state_checkBox_2)

    def set_default_state(self):
        self.checkBoxes[0].setChecked(True)
        self.checkBoxes[1].setChecked(True)
        self.checkBoxes[2].setChecked(True)
        # 使复选框不可改动
        self.checkBoxes[0].setEnabled(False)
        self.apply_monitor_state()

    def apply_monitor_state(self):
        # 按钮状态
        file_path = self.line_edit.text()
        is_file = os.path.isfile(file_path)

        # 设置可用状态
        enabled = all([is_file])
        self.button_import.setEnabled(enabled)

    # 特有方法
    def apply_monitor_state_checkBox_1(self):
        if not self.checkBoxes[1].isChecked() and self.checkBoxes[2].isChecked():
            self.checkBoxes[2].setChecked(False)

    # 特有方法
    def apply_monitor_state_checkBox_2(self):
        if not self.checkBoxes[1].isChecked() and self.checkBoxes[2].isChecked():
            self.checkBoxes[1].setChecked(True)

    # 重写父类方法
    def get_params(self):
        # 导入文件
        file_path = self.line_edit.text()
        # 确定导入道路等级
        if not self.checkBoxes[1].isChecked():
            road_class = 1
        elif self.checkBoxes[1].isChecked() and not self.checkBoxes[2].isChecked():
            road_class = 2
        else:
            road_class = 3

        # 构建参数
        return {
            "file_path": file_path,
            "road_class": road_class,
            "save_data_path": PathConfig.DEFAULT_SAVE_OSM_DIR_PATH,
        }

    # 静态方法：创建路网
    @staticmethod
    def create_network_online(lon_1, lat_1, lon_2, lat_2, parseLevel):
        lon_min = min(lon_1, lon_2)
        lat_min = min(lat_1, lat_2)
        lon_max = max(lon_1, lon_2)
        lat_max = max(lat_1, lat_2)

        road_class = parseLevel

        # 构建参数
        params = {
            "bounding_box": {
                "lon_min": lon_min,
                "lon_max": lon_max,
                "lat_min": lat_min,
                "lat_max": lat_max,
            },
            "road_class": road_class,
            "save_data_path": PathConfig.DEFAULT_SAVE_OSM_DIR_PATH,
        }

        # 构建空类
        class Widget: name, mode, close, utils = "在线导入OSM", "osm", lambda self: None, Utils

        # 执行创建
        MyOperation.apply_import_network(Widget(), params)
