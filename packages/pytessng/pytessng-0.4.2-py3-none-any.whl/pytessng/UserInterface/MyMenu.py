from functools import partial
from PySide2.QtWidgets import QMenu, QAction, QMessageBox

from .Utils import Utils
from .NetworkImport.NetworkImportOpendrive import NetworkImportOpendrive
from .NetworkImport.NetworkImportShape import NetworkImportShape
from .NetworkImport.NetworkImportOpenstreetmap import NetworkImportOpenstreetmap
from .NetworkImport.NetworkImportExcel import NetworkImportExcel
from .NetworkImport.NetworkImportJson import NetworkImportJson
from .NetworkImport.NetworkImportZhecheng import NetworkImportZhecheng
from .NetworkImport.NetworkImportAidaroe import NetworkImportAidaroe
from .NetworkExport.NetworkExportOpendrive import NetworkExportOpendrive
from .NetworkExport.NetworkExportShape import NetworkExportShape
from .NetworkExport.NetworkExportGeojson import NetworkExportGeojson
from .NetworkExport.NetworkExportUnity import NetworkExportUnity
from .NetworkExport.NetworkExportJson import NetworkExportJson
from .LinkEdit.LinkEditCreate import LinkEditCreate
from .LinkEdit.LinkEditSplit import LinkEditSplit
from .LinkEdit.LinkEditMerge import LinkEditMerge
from .LinkEdit.LinkEditSimplify import LinkEditSimplify
from .LinkEdit.LinkEditLimitC import LinkEditLimitC
from .LinkEdit.LinkEditLimitL import LinkEditLimitL
from .LinkEdit.LinkEditModify import LinkEditModify
from .LinkEdit.LinkEditMove import LinkEditMove
from .SimuExport.SimuExportTrajectory import SimuExportTrajectory
from .FileExport.FileExportPilenumber import FileExportPilenumber
from .FileExport.FileExportGrid import FileExportGrid
from .Other.OpenInstruction import OpenInstruction
from .Other.OpenExamples import OpenExamples
from .Other.SendAdvise import SendAdvise
from pytessng.Config import UIConfig
from pytessng.GlobalVar import GlobalVar
from pytessng.DLLs.Tessng import tessngIFace


class MyMenu(QMenu):
    # 按钮名称和类映射
    action_name_and_class_mapping = {
        "network_import": {
            "opendrive": ("action_network_import_opendrive", NetworkImportOpendrive),
            "shape": ("action_network_import_shape", NetworkImportShape),
            "osm": ("action_network_import_openstreetmap", NetworkImportOpenstreetmap),
            "excel": ("action_network_import_excel", NetworkImportExcel),
            "json": ("action_network_import_json", NetworkImportJson),
            "zhecheng": ("action_network_import_zhecheng", NetworkImportZhecheng),
            "aidaroe": ("action_network_import_aidaroe", NetworkImportAidaroe),
        },
        "network_export": {
            "opendrive": ("action_network_export_opendrive", NetworkExportOpendrive),
            "shape": ("action_network_export_shape", NetworkExportShape),
            "geojson": ("action_network_export_geojson", NetworkExportGeojson),
            "unity": ("action_network_export_unity", NetworkExportUnity),
            "json": ("action_network_export_json", NetworkExportJson),
        },
        "link_edit": {
            "create": ("action_link_edit_create", LinkEditCreate),
            "split": ("action_link_edit_split", LinkEditSplit),
            "merge": ("action_link_edit_merge", LinkEditMerge),
            "simplify": ("action_link_edit_simplify", LinkEditSimplify),
            "limit_c": ("action_link_edit_limit_c", LinkEditLimitC),
            "limit_l": ("action_link_edit_limit_l", LinkEditLimitL),
            "modify": ("action_link_edit_modify", LinkEditModify),
            "move": ("action_link_edit_move", LinkEditMove),
        },
        "simu_data_export": {
            "trajectory": ("action_simu_export_trajectory", SimuExportTrajectory),
        },
        "config_file_export": {
            "pilenumber": ("action_file_export_pilenumber", FileExportPilenumber),
            "grid": ("action_file_export_grid", FileExportGrid),
        },
        "other": {
            "instruction": ("action_other_instruction", OpenInstruction),
            "examples": ("action_other_examples", OpenExamples),
            "advise": ("action_other_advise", SendAdvise),
        }
    }
    # 工具包
    utils = Utils

    def __init__(self, *args, extension=False):
        super().__init__(*args)
        # 是否功能拓展
        self.extension = extension
        # 当前菜单
        self.current_dialog = None

        # 初始化
        self.init()

    def init(self):
        self.setObjectName("pytessng")
        self.setTitle("数据导入导出")

        # 添加菜单
        self.set_action()
        # 设置隐藏（配置项）
        self.set_hide()
        # 关联槽函数
        self.set_connect()

        # 统计用户数量
        self.utils.send_message("operation", "visit")

        # 关联槽函数
        iface = tessngIFace()
        win = iface.guiInterface().mainWindow()
        win.forPythonOsmInfo.connect(NetworkImportOpenstreetmap.create_network_online)

    def set_action(self):
        # =============== 1.路网创建 ===============
        self.menu_network_import = self.addMenu('路网创建')
        # 1.1.导入OpenDrive
        self.action_network_import_opendrive = self.menu_network_import.addAction('导入OpenDrive (.xodr)')
        # 1.2.导入Shape
        self.action_network_import_shape = self.menu_network_import.addAction('导入Shape')
        # 1.3.导入OpenStreetMap
        self.action_network_import_openstreetmap = self.menu_network_import.addAction('导入OpenStreetMap')
        # 1.4.导入Excel
        self.action_network_import_excel = self.menu_network_import.addAction('导入Excel (.xlsx/.xls/.csv)')
        # 1.5.导入Json
        self.action_network_import_json = self.menu_network_import.addAction('导入Json')
        # 1.6.导入浙诚数据
        # self.action_network_import_zhecheng = self.menu_network_import.addAction('导入浙诚数据 (.json)')
        # 1.7.导入Aidaroe
        self.action_network_import_aidaroe = self.menu_network_import.addAction('导入Aidaroe (.jat)')

        # =============== 2.路网数据导出 ===============
        self.menu_network_export = self.addMenu('路网数据导出')
        # 2.1.导出OpenDrive
        self.action_network_export_opendrive = self.menu_network_export.addAction('导出为OpenDrive (.xodr)')
        # 2.2.导出Shape
        self.action_network_export_shape = self.menu_network_export.addAction('导出为Shape')
        # 2.3.导出GeoJson
        self.action_network_export_geojson = self.menu_network_export.addAction('导出为GeoJson')
        # 2.4.导出Unity
        self.action_network_export_unity = self.menu_network_export.addAction('导出为Unity (.json)')
        # 2.5.导出Json
        self.action_network_export_json = self.menu_network_export.addAction('导出为Json')

        # =============== 3.路段编辑 ===============
        self.menu_link_edit = self.addMenu('路段编辑')
        # 3.1.创建路段
        self.action_link_edit_create = self.menu_link_edit.addAction('创建路段')
        # 3.2.打断路段
        self.action_link_edit_split = QAction("打断路段")
        self.menu_link_edit.addAction(self.action_link_edit_split)
        self.action_link_edit_split.setCheckable(True)  # 开启是否勾选
        self.action_link_edit_split.setEnabled(False)  # 为了判断是不是试用版
        GlobalVar.action_network_edit_split = self.action_link_edit_split  # 为了判断是不是试用版
        # 3.3.合并路段
        self.action_link_edit_merge = self.menu_link_edit.addAction('合并路段（路网级）')
        # 3.4.简化路段点位
        self.action_link_edit_simplify = self.menu_link_edit.addAction('简化路段点位（路网级）')
        # 3.5.限制连接段最小长度
        self.action_link_edit_limit_c = self.menu_link_edit.addAction('限制连接段最小长度（路网级）')
        # 3.6.限制路段最大长度
        self.action_link_edit_limit_l = self.menu_link_edit.addAction('限制路段最大长度（路网级）')
        # 3.7.修改路段限速
        self.action_link_edit_modify = self.menu_link_edit.addAction('修改路段限速（路网级）')
        # 3.8.移动路网
        self.action_link_edit_move = self.menu_link_edit.addAction('移动路网')

        # =============== 4.仿真数据导出 ===============
        self.menu_simu_export = self.addMenu('仿真数据导出')
        # 4.1.导出轨迹数据
        self.action_simu_export_trajectory = QAction("导出轨迹数据")
        self.menu_simu_export.addAction(self.action_simu_export_trajectory)
        self.action_simu_export_trajectory.setEnabled(False)  # 为了判断是不是试用版
        GlobalVar.action_simu_export_trajectory = self.action_simu_export_trajectory  # 为了判断是不是试用版

        # =============== 5.项目配置文件导出 ===============
        self.menu_file_export = self.addMenu('项目配置文件导出')
        # 5.1.导出桩号数据
        self.action_file_export_pilenumber = self.menu_file_export.addAction('导出桩号数据')
        # 5.2.导出选区数据
        self.action_file_export_grid = QAction("导出选区数据")
        self.menu_file_export.addAction(self.action_file_export_grid)
        self.action_file_export_grid.setCheckable(True)  # 开启是否勾选
        self.action_file_export_grid.setEnabled(False)  # 为了判断是不是试用版
        GlobalVar.action_file_export_grid = self.action_file_export_grid  # 为了判断是不是试用版

        # =============== 6.更多 ===============
        self.menu_other = self.addMenu('更多')
        # 5.1.打开说明书
        self.action_other_instruction = self.menu_other.addAction("打开说明书")
        # 5.2.打开样例
        self.action_other_examples = self.menu_other.addAction("打开路网创建样例")
        # 5.3.提出建议
        self.action_other_advise = self.menu_other.addAction("提交用户反馈")

    # 设置按钮隐藏
    def set_hide(self):
        # 如果是完整版
        if self.extension:
            return

        # 设置隐藏
        for first_class, second_class_list in UIConfig.Menu.extension_list:
            try:
                # 如果是列表就单个隐藏
                if type(second_class_list) == list:
                    for second_class in second_class_list:
                        action_name = f"action_{first_class}_{second_class}"
                        action = getattr(self, action_name)
                        action.setVisible(False)
                # 如果不是列表就是全部隐藏
                else:
                    menu_name = f"menu_{first_class}"
                    menu = getattr(self, menu_name)
                    menu.menuAction().setVisible(False)
            except:
                pass

    # 将按钮与函数关联
    def set_connect(self):
        for first_class, second_class_mapping in self.action_name_and_class_mapping.items():
            for second_class, action_and_class in second_class_mapping.items():
                # 获取按钮名称
                action_name = action_and_class[0]
                # 如果有这个按钮，而且也不是None
                if hasattr(self, action_name):
                    # 获取按钮
                    action = getattr(self, action_name)
                    # 关联函数
                    action.triggered.connect(partial(self.apply_action, first_class, second_class))

    # 执行操作
    def apply_action(self, frist_class: str, second_class: str):
        # =============== 特殊情况特殊处理 ===============
        if frist_class == "network_import" and second_class == "osm":
            messages = {
                "title": "OSM导入模式",
                "content": "请选择导入离线文件或获取在线地图",
                "yes": "导入离线文件",
                "no": "获取在线地图",
            }
            result = Utils.show_confirm_dialog(messages)

            # No键
            if result == QMessageBox.No:
                iface = tessngIFace()
                win = iface.guiInterface().mainWindow()
                # 显示在线地图
                win.showOsmInline(True)
                return
            # 取消键
            elif result == QMessageBox.Cancel:
                return
        # =============================================

        try:
            # 获取对应类
            action_class = self.action_name_and_class_mapping[frist_class][second_class][1]
            dialog = action_class()
            # 关闭上一个窗口
            if self.current_dialog:
                self.current_dialog.close()
            # 显示窗口
            if dialog:
                self.current_dialog = dialog
                self.current_dialog.load()
                self.current_dialog.show()
        except:
            self.utils.show_info_box("该功能暂未开放！")
