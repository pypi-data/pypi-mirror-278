import os
import traceback
from PySide2.QtWidgets import QMessageBox
from PySide2.QtCore import QPointF

from .NetworkImport.Other2TessngFactory import Other2TessngFactory
from .NetworkExport.Tessng2OtherFactory import Tessng2OtherFactory
from .LinkEdit.LinkEditorFactory import LinkEditorFactory
from .FileExport.PilenumberDataSaver import PilenumberDataSaver
from .FileExport.GridDataSaver import GridDataSaver
from pytessng.Config import PathConfig
from pytessng.Logger import logger
from pytessng.ProgressDialog import ProgressDialogClass
from pytessng.DLLs.Tessng import tessngIFace


class MyOperation:
    # 创建路网
    @staticmethod
    def apply_import_network(widget, params: dict):
        iface = tessngIFace()
        netiface = iface.netInterface()
        simuiface = iface.simuInterface()
        guiiface = iface.guiInterface()

        # 1.更改默认路径
        path = params.get("folder_path") or params.get("file_path")
        if path:
            PathConfig.OPEN_DIR_PATH = os.path.dirname(path)

        # 2.正在仿真中无法导入
        if iface.simuInterface().isRunning() or iface.simuInterface().isPausing():
            widget.utils.show_info_box("请先停止仿真！", "warning")
            return

        # 3.路网上已经有路段进行询问
        link_count = netiface.linkCount()
        if link_count > 0:
            messages = {
                "title": "是否继续",
                "content": "路网上已有路段，请选择是否继续导入",
                "yes": "继续",
            }
            confirm = widget.utils.show_confirm_dialog(messages)
            if confirm != QMessageBox.Yes:
                return

        # 4.尝试关闭在线地图
        win = guiiface.mainWindow()
        win.showOsmInline(False)

        # 5.关闭窗口
        widget.close()

        # 6.执行转换
        try:
            # 记录日志
            logger.logger_pytessng.info(f"Network import mode: {widget.mode}")
            logger.logger_pytessng.info(f"Network import params: {params}")

            # 当前路网上的路段ID
            current_linkIds = netiface.linkIds()

            # 创建路段
            response = Other2TessngFactory.build(netiface, widget.mode, params)
            status, message = response["status"], response["message"]

            # 如果有问题
            if not status:
                message, mode = message, "warning"
            # 如果没问题，问要不要移动
            else:
                # 新创建的路段
                new_links = [link for link in netiface.links() if link.id() not in current_linkIds]
                xs, ys = [], []
                for link in new_links:
                    points = link.centerBreakPoints()
                    xs.extend([point.x() for point in points])
                    ys.extend([point.y() for point in points])

                if xs and ys:
                    x_min, x_max = min(xs), max(xs)
                    y_min, y_max = min(ys), max(ys)
                    message = f"新创建路网的范围：\n    x = [ {x_min:.1f} m , {x_max:.1f} m ]\n    y = [ {y_min:.1f} m , {y_max:.1f} m ]\n"

                    # osm自动移动，其他要询问
                    if widget.mode != "osm":
                        messages = {
                            "title": "是否移动至中心",
                            "content": message + "是否将路网移动到场景中心",
                            "yes": "确定",
                        }
                        confirm = widget.utils.show_confirm_dialog(messages)

                        # 移动
                        attrs = netiface.netAttrs().otherAttrs()
                        if confirm == QMessageBox.Yes:
                            # 比例尺转换
                            scene_scale = netiface.sceneScale()
                            x_move = attrs["move_distance"]["x_move"] / scene_scale
                            y_move = attrs["move_distance"]["y_move"] / scene_scale
                            # 移动路网
                            move = QPointF(x_move, -y_move)
                            netiface.moveLinks(new_links, move)
                        # 不移动
                        else:
                            attrs.update({"move_distance": {"x_move": 0, "y_move": 0}})
                            netiface.setNetAttrs("Network", otherAttrsJson=attrs)

                message, mode = "导入成功", "info"
            logger.logger_pytessng.info(f"Network attrs: {netiface.netAttrs().otherAttrs()}")

        except:
            message, mode = "导入失败", "warning"
            logger.logger_pytessng.critical(traceback.format_exc())

        # 7.设置场景宽度和高度
        all_links = netiface.links()
        if all_links:
            xs, ys = [], []
            for link in all_links:
                points = link.centerBreakPoints()
                xs.extend([point.x() for point in points])
                ys.extend([point.y() for point in points])
            width = max(max(abs(max(xs)), abs(min(xs))) * 2 + 10, 600)
            height = max(max(abs(max(ys)), abs(min(ys))) * 2 + 10, 400)
            netiface.setSceneSize(width, height)  # m

        # 8.设置不限时长
        simuiface.setSimuIntervalScheming(0)

        # 9.关闭进度条
        ProgressDialogClass().close()

        # 10.打印属性信息
        attrs = netiface.netAttrs().otherAttrs()
        print("=" * 66)
        print("Create network! Network attrs:")
        for k, v in attrs.items():
            print(f"\t{k:<15}:{' '*5}{v}")
        print("=" * 66, "\n")

        # 11.弹出提示框
        widget.utils.show_info_box(message, mode)

        # 12.记录信息
        widget.utils.send_message("operation", widget.name)

    # 路网导出
    @staticmethod
    def apply_export_network(widget):
        iface = tessngIFace()
        netiface = iface.netInterface()
        simuiface = iface.simuInterface()

        # 1.正在仿真中无法导出
        if simuiface.isRunning() or simuiface.isPausing():
            widget.utils.show_info_box("请先停止仿真！", "warning")
            return

        # 2.检查路网上是否有路段
        if netiface.linkCount() == 0:
            widget.utils.show_info_box("当前路网没有路段 !", "warning")
            return

        # 3.获取投影
        if hasattr(widget, 'checkBox'):
            isChecked = widget.checkBox.isChecked()
        elif hasattr(widget, 'radio_coord_2'):
            isChecked = widget.radio_coord_2.isChecked()
        else:
            isChecked = False
        if isChecked:
            if widget.radio_proj_custom.isChecked():
                lon_0 = float(widget.lineEdit_proj_custom_lon.text())
                lat_0 = float(widget.lineEdit_proj_custom_lat.text())
                proj_string = f'+proj=tmerc +lon_0={lon_0} +lat_0={lat_0} +ellps=WGS84'
            else:
                proj_string = widget.file_proj_string
        else:
            proj_string = ""

        # 4.获取保存路径
        file_path = widget.utils.save_file(widget.format)
        if not file_path:
            return
        # 更改默认路径
        PathConfig.OPEN_DIR_PATH = os.path.dirname(file_path)

        # 5.关闭窗口
        widget.close()

        # 6.执行转换
        logger.logger_pytessng.info(f"Network export mode: {widget.mode}")
        params = {"proj_string": proj_string, "file_path": file_path}
        logger.logger_pytessng.info(f"Network export params: {params}")
        logger.logger_pytessng.info(f"Network attrs: {netiface.netAttrs().otherAttrs()}")
        Tessng2OtherFactory.build(netiface, widget.mode, params)

        # 7.关闭进度条
        ProgressDialogClass().close()

        # 8.提示信息
        widget.utils.show_info_box("保存成功！")

        # 9.记录信息
        widget.utils.send_message("operation", widget.name)

    # 编辑路段
    @staticmethod
    def apply_edit_link(widget, params: dict):
        iface = tessngIFace()
        netiface = iface.netInterface()
        simuiface = iface.simuInterface()

        # 1.正在仿真中无法导出
        if simuiface.isRunning() or simuiface.isPausing():
            widget.utils.show_info_box("请先停止仿真！", "warning")
            return

        # 2.检查有无路段
        if widget.mode in ["merge", "simplify", "limit_c", "limit_l", "modify", "move"]:
            # 如果没有路段
            if not netiface.linkCount():
                widget.utils.show_info_box("当前路网没有路段！", "warning")
                return

        # 3.关闭窗口
        widget.close()

        # 4.执行路段编辑
        logger.logger_pytessng.info(f"Link edit mode: {widget.mode}")
        logger.logger_pytessng.info(f"Link edit params: {params}")
        try:
            LinkEditorFactory.build(widget.mode, netiface, params)
            message, mode = "操作成功", "info"
        except:
            logger.logger_pytessng.critical(traceback.format_exc())
            message, mode = "操作失败", "warning"

        # 5.关闭进度条
        ProgressDialogClass().close()

        # 6.提示信息
        widget.utils.show_info_box(message, mode)

        # 7.记录信息
        widget.utils.send_message("operation", widget.name)

    # 其他操作
    @staticmethod
    def apply_other_operation(widget, params: dict):
        operator_mapping = {
            "pilenumber": PilenumberDataSaver,
            "grid": GridDataSaver,
        }

        iface = tessngIFace()
        netiface = iface.netInterface()
        simuiface = iface.simuInterface()
        guiiface = iface.guiInterface()

        # 1.正在仿真中无法导出
        if simuiface.isRunning() or simuiface.isPausing():
            widget.utils.show_info_box("请先停止仿真！", "warning")
            return

        # 2.将按钮修改成【取消工具】
        guiiface.actionNullGMapTool().trigger()

        # 3.获取保存路径
        file_path = widget.utils.save_file(widget.format)
        if not file_path:
            return
        # 更改默认路径
        PathConfig.OPEN_DIR_PATH = os.path.dirname(file_path)

        # 4.关闭窗口
        widget.close()

        # 5.执行操作
        logger.logger_pytessng.info(f"Other operation mode: {widget.mode}")
        logger.logger_pytessng.info(f"Other operation params: {params}")
        operator = operator_mapping.get(widget.mode)
        if not operator:
            return
        try:
            operator(netiface).export(**params, file_path=file_path)
            message, mode = "操作完成", "info"
        except:
            logger.logger_pytessng.critical(traceback.format_exc())
            message, mode = "操作失败", "warning"

        # 6.关闭进度条
        ProgressDialogClass().close()

        # 7.提示信息
        widget.utils.show_info_box(message, mode)

        # 8.记录信息
        widget.utils.send_message("operation", widget.name)
