from typing import Callable
from functools import partial
from PySide2.QtWidgets import QLabel, QLineEdit, QPushButton, QMenu, QAction
from PySide2.QtGui import QDoubleValidator
from PySide2.QtCore import Qt

from .BaseLinkEdit import BaseLinkEdit, MyQHBoxLayout, MyQVBoxLayout
from pytessng.Config import LinkEditConfig
from pytessng.GlobalVar import GlobalVar
from pytessng.ToolInterface import MyOperation
from pytessng.ToolInterface import LinkEditorFactory


class LinkEditSplit(BaseLinkEdit):
    name: str = "通过坐标打断路段"
    mode: str = "split"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 按钮
        self.action = GlobalVar.action_network_edit_split
        # 定位者
        self.locator = None

    # 重写抽象父类BaseUserInterface的方法
    def load(self):
        # 开启
        if self.action.isChecked():
            self.action.setChecked(True)
            GlobalVar.is_need_select_network_edit_split = True
            super().load()
        # 关闭
        else:
            self.action.setChecked(False)
            GlobalVar.is_need_select_network_edit_split = False
            self.after_stop()

    # 重写父类QWidget的方法
    def show(self):
        if self.action.isChecked():
            super().show()

    # 特有方法：关闭打断路段功能之后
    def after_stop(self):
        # 修改状态
        self.action.setChecked(False)
        # 修改文字
        self.action.setText("打断路段")
        # 释放定位者
        self.locator = None
        # 关闭回调函数
        GlobalVar.function_network_edit_split = None

    def set_widget_layout(self):
        # 第一行：文本、下拉框、文本、输入框
        self.label_length = QLabel('连接段最小长度（m）：')
        self.line_edit_length = QLineEdit()
        # self.line_edit_length.setFixedWidth(100)
        # 第二行：按钮
        self.button = QPushButton('确定')

        # 总体布局
        layout = MyQVBoxLayout([
            MyQHBoxLayout([self.label_length, self.line_edit_length]),
            self.button
        ])
        self.setLayout(layout)

        # 限制输入框内容
        validator = QDoubleValidator()
        self.line_edit_length.setValidator(validator)

        # 设置提示信息
        min_min_connector_length = LinkEditConfig.MIN_MIN_CONNECTOR_LENGTH
        max_min_connector_length = LinkEditConfig.MAX_MIN_CONNECTOR_LENGTH
        self.line_edit_length.setToolTip(f'{min_min_connector_length} <= length <= {max_min_connector_length}')

    def set_monitor_connect(self):
        self.line_edit_length.textChanged.connect(self.apply_monitor_state)

    def set_default_state(self):
        default_min_connector_length = LinkEditConfig.DEFAULT_MIN_CONNECTOR_LENGTH
        self.line_edit_length.setText(f"{default_min_connector_length}")
        self.apply_monitor_state()

    def apply_monitor_state(self):
        length = self.line_edit_length.text()
        # 按钮状态
        enabled_button = False
        try:
            length = float(length)
            min_min_connector_length = LinkEditConfig.MIN_MIN_CONNECTOR_LENGTH
            max_min_connector_length = LinkEditConfig.MAX_MIN_CONNECTOR_LENGTH
            if min_min_connector_length <= float(length) <= max_min_connector_length:
                enabled_button = True
        except:
            pass

        # 设置可用状态
        self.button.setEnabled(enabled_button)

    # 重写父类方法
    def apply_button_action(self):
        # 获取按钮状态
        if self.action.isChecked():
            # 修改文字
            self.action.setText("取消选中打断路段")

            # 修改按钮为【取消工具】
            guiiface = self.iface.guiInterface()
            guiiface.actionNullGMapTool().trigger()
            # 把其他关联上
            for actions in [guiiface.netToolBar().actions(), guiiface.operToolBar().actions()]:
                for action in actions:
                    if action.text() == "取消工具":
                        continue
                    action.triggered.connect(self.after_stop)

            # 创建定位者并传递回调函数
            self.locator = LinkEditLocate(self.apply_split_link, self.iface)
            GlobalVar.function_network_edit_split = self.locator.handle_mouse_event

            # 关闭窗口
            self.close()
            # 显示提示信息
            self.utils.show_info_box("请右击需要打断的位置来打断路段！")

    # 特有方法：编辑路段
    def apply_split_link(self, params: dict, on_success: Callable = None):
        if on_success:
            on_success()

        params = {
            **params,
            "min_connector_length": float(self.line_edit_length.text())
        }
        # 执行路段编辑
        MyOperation.apply_edit_link(self, params)


class LinkEditLocate:
    name: str = "通过坐标定位路段"
    mode: str = "locate"

    def __init__(self, apply_split_link_func: Callable, iface):
        # 按钮
        self.action = GlobalVar.action_network_edit_split
        # 菜单栏
        self.context_menu = None
        # 执行路段编辑的函数
        self.apply_split_link_func = apply_split_link_func

        # TESSNG接口
        self.iface = iface
        self.guiiface = self.iface.guiInterface()
        self.netiface = self.iface.netInterface()

    # 处理鼠标事件
    def handle_mouse_event(self, event):
        if self.action.isChecked():
            # 将按钮修改成【取消工具】
            self.guiiface.actionNullGMapTool().trigger()

            # 如果是右击
            if event.button() == Qt.RightButton:
                # 在TESSNG中的坐标
                pos = self.netiface.graphicsView().mapToScene(event.pos())
                # 定位路段
                params = {"pos": pos}
                link_id_list = LinkEditorFactory.build(self.mode, self.netiface, params=params)
                # 创建菜单栏
                self.create_context_menu(link_id_list, pos)

    # 创建菜单栏
    def create_context_menu(self, link_id_list, pos):
        guiiface = self.iface.guiInterface()
        # 获取界面
        win = guiiface.mainWindow()
        # 创建菜单栏
        self.context_menu = QMenu(win)
        # 在菜单中添加动作
        for link_id in link_id_list:
            action = QAction(f"打断路段[{link_id}]", win)
            params = {"link_id": link_id, "pos": pos}
            action.triggered.connect(partial(self.apply_split_link_func, params, self.delete_context_menu))
            self.context_menu.addAction(action)
        self.context_menu.addAction(self.action)
        # 设置右击事件
        win.setContextMenuPolicy(Qt.CustomContextMenu)
        win.customContextMenuRequested.connect(self.show_context_menu)

    # 显示菜单栏：在鼠标位置显示
    def show_context_menu(self, pos):
        if self.action.isChecked() and self.context_menu is not None:
            win = self.iface.guiInterface().mainWindow()
            self.context_menu.exec_(win.mapToGlobal(pos))

    # 删除菜单栏
    def delete_context_menu(self):
        if self.context_menu is not None:
            self.context_menu.close()
            self.context_menu = None
