from PySide2.QtWidgets import QProgressDialog
from PySide2.QtCore import Qt, QCoreApplication
from PySide2.QtGui import QIcon

from pytessng.Config import PathConfig


class ProgressDialogClass(QProgressDialog):
    _instance = None
    _init = False
    def __new__(cls,):
        if ProgressDialogClass._instance is None:
            ProgressDialogClass._instance = super().__new__(cls)
        return ProgressDialogClass._instance

    def __init__(self):
        if ProgressDialogClass._init:
            return
        ProgressDialogClass._init = True

        super(ProgressDialogClass, self).__init__()
        self.setWindowTitle('进度条')
        self.setWindowIcon(QIcon(PathConfig.ICON_FILE_PATH))
        self.setCancelButton(None)  # 禁用取消按钮
        self.setRange(0, 100+1)
        self.setValue(0)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)  # 设置窗口显示在最上面
        self.setFixedWidth(400)

    # 更新进度条
    def update_progress(self, index, all_count, new_text=""):
        self.setLabelText(new_text)
        new_value = int(round(index / all_count * 100, 0))
        self.setValue(new_value)
        self.show()
        # 立刻更新界面
        QCoreApplication.processEvents()

    # 包裹器
    @staticmethod
    def progress(iterable_items, text=""):
        iterable_items_list = list(iterable_items)
        all_count = len(iterable_items_list)
        ProgressDialogClass().setValue(0)
        for index, item in enumerate(iterable_items_list):
            yield item
            ProgressDialogClass().update_progress(index + 1, all_count, text)
        # ProgressDialogClass().hide()  # TODO 进度条结束后隐藏
