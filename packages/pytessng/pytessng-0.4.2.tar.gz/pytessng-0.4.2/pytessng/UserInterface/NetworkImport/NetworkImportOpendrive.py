import os
from PySide2.QtWidgets import QLineEdit, QPushButton, QLabel, QComboBox, QCheckBox
from PySide2.QtCore import Qt

from .BaseNetworkImport import BaseNetworkImport, MyQHBoxLayout, MyQVBoxLayout


class NetworkImportOpendrive(BaseNetworkImport):
    name: str = "导入OpenDrive"
    mode: str = "opendrive"
    format: list = [("OpenDrive", "xodr")]

    def set_widget_layout(self):
        # 第一行：文本框和按钮
        self.line_edit = QLineEdit()
        self.line_edit.setFixedWidth(500)
        self.button_select = QPushButton('文件选择')
        # 第二行：文本和下拉框
        self.label_select_length = QLabel("路段最小分段长度：")
        self.combo = QComboBox()
        self.combo.addItems(("1 m", "3 m", "5 m", "10 m", "20 m"))
        # 第三行：文本框
        self.label_select_type = QLabel("生成车道类型：")
        # 第四行：多选栏
        self.checkBoxes = [
            QCheckBox('机动车道'),
            QCheckBox('非机动车道'),
            QCheckBox('人行道'),
            QCheckBox('应急车道')
        ]
        # 第五行：按钮
        self.button_import = QPushButton('生成路网文件')

        # 总体布局
        layout = MyQVBoxLayout([
            MyQHBoxLayout([self.line_edit, self.button_select]),
            MyQHBoxLayout([self.label_select_length, self.combo]),
            self.label_select_type,
            MyQHBoxLayout(self.checkBoxes),
            self.button_import,
        ])
        self.setLayout(layout)

    def set_monitor_connect(self):
        self.line_edit.textChanged.connect(self.apply_monitor_state)
        for checkBox in self.checkBoxes:
            checkBox.stateChanged.connect(self.apply_monitor_state)

    def set_default_state(self):
        self.combo.setCurrentIndex(0)
        for checkBox in self.checkBoxes:
            checkBox.setCheckState(Qt.Checked)
        self.apply_monitor_state()

    def apply_monitor_state(self):
        file_path = self.line_edit.text()
        is_file = os.path.isfile(file_path)

        checkbox_isChecked = any(checkbox.isChecked() for checkbox in self.checkBoxes)

        # 设置可用状态
        enabled = all([is_file, checkbox_isChecked])
        self.button_import.setEnabled(enabled)

    # 重写父类方法
    def get_params(self):
        # 获取文件名
        file_path = self.line_edit.text()
        # 获取分段长度
        step_length = float(self.combo.currentText().split()[0])
        # 获取车道类型
        lane_types = [checkbox.text() for checkbox in self.checkBoxes if checkbox.isChecked()]

        # 构建参数
        return {
            "file_path": file_path,
            "step_length": step_length,
            "lane_types": lane_types,
        }
