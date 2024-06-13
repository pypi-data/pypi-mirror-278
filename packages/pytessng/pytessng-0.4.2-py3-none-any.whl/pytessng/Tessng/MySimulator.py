from pytessng.DLLs.Tessng import PyCustomerSimulator, tessngIFace
from pytessng.ToolInterface import SimuExportTrajectoryActor


class MySimulator(PyCustomerSimulator):
    def __init__(self):
        super().__init__()
        self.export_traj_actor = SimuExportTrajectoryActor()

    # 每次仿真前
    def beforeStart(self, ref_keepOn):
        iface = tessngIFace()
        netiface = iface.netInterface()

        self.export_traj_actor.ready(netiface)

    # 每次仿真后
    def afterStop(self):
        self.export_traj_actor.finish()

    # 每帧仿真后
    def afterOneStep(self):
        iface = tessngIFace()
        simuiface = iface.simuInterface()

        # 发送轨迹数据
        self.export_traj_actor.send(simuiface)
