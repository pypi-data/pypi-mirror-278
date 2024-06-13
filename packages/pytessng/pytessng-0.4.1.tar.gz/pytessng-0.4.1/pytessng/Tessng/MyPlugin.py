from .MyNet import MyNet
from .MySimulator import MySimulator
from pytessng.DLLs.Tessng import TessPlugin, tessngIFace
from pytessng.UserInterface import MyMenu


class MyPlugin(TessPlugin):
    def __init__(self, extension):
        super(MyPlugin, self).__init__()
        self.my_menu = None
        self.my_net = None
        self.my_simulator = None

        # 功能拓展
        self.extension = extension

    # 过载父类方法，在 TESS NG工厂类创建TESS NG对象时调用
    def init(self):
        iface = tessngIFace()
        guiiface = iface.guiInterface()

        # 增加菜单及菜单项
        menuBar = guiiface.menuBar()
        self.my_menu = MyMenu(menuBar, extension=self.extension)
        menuBar.insertAction(menuBar.actions()[-1], self.my_menu.menuAction())

        self.my_net = MyNet()
        self.my_simulator = MySimulator()

        # 关闭在线地图
        win = guiiface.mainWindow()
        win.showOsmInline(False)

    # 过载父类方法，返回插件路网子接口，此方法由TESS NG调用
    def customerNet(self):
        return self.my_net

    #过载父类方法，返回插件仿真子接口，此方法由TESS NG调用
    def customerSimulator(self):
        return self.my_simulator
