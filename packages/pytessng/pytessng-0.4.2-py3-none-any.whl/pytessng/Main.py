import os
import sys
import shutil
from warnings import filterwarnings
from PySide2.QtWidgets import QApplication

from pytessng.DLLs.Tessng import TessngFactory
from pytessng.Tessng.MyPlugin import MyPlugin


class TessngObject:
    def __init__(self, extension: bool = False):
        # 工作空间是本进程所在的路径
        self.workspace_path = os.path.join(os.getcwd(), "WorkSpace")
        # 加载之前
        self.before_run()
        # 加载
        self.run(extension)

    def before_run(self):
        # 创建工作空间文件夹
        os.makedirs(self.workspace_path, exist_ok=True)
        # 本文件所在文件夹的路径
        this_file_path = os.path.dirname(__file__)

        # =============== 1. 移动试用版key ===============
        # 试用版key的位置
        cert_file_path = os.path.join(this_file_path, "Files", "Cert", "JidaTraffic_key")
        # 移动后的位置
        cert_folder_path = os.path.join(self.workspace_path, "Cert")
        new_cert_file_path = os.path.join(cert_folder_path, "可使用本试用版密钥激活TESSNG")
        # 如果不存在就复制移动
        if not os.path.exists(cert_folder_path):
            os.makedirs(cert_folder_path, exist_ok=True)
            shutil.copy(cert_file_path, new_cert_file_path)

        # =============== 2. 移动导入样例 ===============
        # 导入样例的位置
        examples_file_path = os.path.join(this_file_path, "Files", "Examples")
        # 移动后的位置
        new_examples_file_path = os.path.join(self.workspace_path, "Examples")
        try:
            shutil.copytree(examples_file_path, new_examples_file_path)
        except:
            pass

        # =============== 3. 忽略警告 ===============
        filterwarnings("ignore")

    def run(self, extension: bool):
        app = QApplication()
        config = {
            '__workspace': self.workspace_path,  # 工作空间
            '__simuafterload': False,  # 加载路网后是否自动启动仿真
            '__custsimubysteps': False,  # 是否自定义仿真调用频率
            '__allowspopup': False,  # 禁止弹窗
            '__cacheid': True,  # 快速创建路段
        }
        plugin = MyPlugin(extension)
        factory = TessngFactory()
        tessng = factory.build(plugin, config)
        if tessng is not None:
            sys.exit(app.exec_())
        else:
            sys.exit()
