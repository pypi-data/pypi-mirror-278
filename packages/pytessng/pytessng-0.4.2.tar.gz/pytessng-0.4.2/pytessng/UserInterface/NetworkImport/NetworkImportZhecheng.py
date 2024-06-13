import os
from functools import partial
from PySide2.QtWidgets import QLineEdit, QPushButton

from .BaseNetworkImport import BaseNetworkImport, MyQHBoxLayout, MyQVBoxLayout


class NetworkImportZhecheng(BaseNetworkImport):
    name: str = "导入Zhecheng"
    mode: str = "zhecheng"
    format: list = [("Json", "json")]

    def set_widget_layout(self) -> None:
        # 第一行：文本框和按钮
        self.line_edit_1 = QLineEdit()
        self.line_edit_1.setFixedWidth(500)
        self.button_select_1 = QPushButton('车道Shp文件夹选择')
        # 第二行：文本框和按钮
        self.line_edit_2 = QLineEdit()
        self.line_edit_2.setFixedWidth(500)
        self.button_select_2 = QPushButton('附属信息文件选择')
        # 第三行：按钮
        self.button_import = QPushButton('生成路网文件')

        # 总体布局
        layout = MyQVBoxLayout([
            MyQHBoxLayout([self.line_edit_1, self.button_select_1]),
            MyQHBoxLayout([self.line_edit_2, self.button_select_2]),
            self.button_import
        ])
        self.setLayout(layout)

    def set_monitor_connect(self) -> None:
        self.line_edit_1.textChanged.connect(self.apply_monitor_state)
        self.line_edit_2.textChanged.connect(self.apply_monitor_state)

    def set_button_connect(self) -> None:
        self.button_select_1.clicked.connect(partial(self.select_folder, self.line_edit_1))
        self.button_select_2.clicked.connect(partial(self.select_file, self.line_edit_2))
        self.button_import.clicked.connect(self.apply_button_action)

    def apply_monitor_state(self) -> None:
        folder_path = self.line_edit_1.text()
        is_dir = os.path.isdir(folder_path)
        file_path = self.line_edit_2.text()
        is_file = os.path.isfile(file_path)

        # 设置可用状态
        enabled = all([is_dir, is_file])
        self.button_import.setEnabled(enabled)

    # 重写父类方法
    def get_params(self) -> dict:
        # 获取文件夹路径
        folder_path = self.line_edit_1.text()
        # 获取文件路径
        file_path = self.line_edit_2.text()

        return {
            "folder_path": folder_path,
            "file_path": file_path,
        }
