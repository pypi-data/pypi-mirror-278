from PySide2.QtWidgets import QPushButton, QCheckBox

from .BaseLinkEdit import BaseLinkEdit, MyQHBoxLayout, MyQVBoxLayout


class LinkEditMerge(BaseLinkEdit):
    name: str = "合并路段"
    mode: str = "merge"

    def set_widget_layout(self):
        # 第一行：勾选框
        self.checkbox_1 = QCheckBox("是否使用连接段点位")
        # 第二行：勾选框
        self.checkbox_2 = QCheckBox("是否简化点位")
        # 第三行：按钮
        self.button = QPushButton('合并路段')

        # 总体布局
        layout = MyQVBoxLayout([
            MyQHBoxLayout([self.checkbox_1, self.checkbox_2]),
            self.button
        ])
        self.setLayout(layout)

    def set_default_state(self):
        self.checkbox_1.setChecked(True)
        self.checkbox_2.setChecked(True)

    # 重写父类方法
    def get_params(self) -> dict:
        include_connector = self.checkbox_1.isChecked()
        simplify_points = self.checkbox_2.isChecked()
        return {
            "include_connector": include_connector,
            "simplify_points": simplify_points
        }
