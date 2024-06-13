from pytessng.DLLs.Tessng import PyCustomerNet, tessngIFace
from pytessng.GlobalVar import GlobalVar


class MyNet(PyCustomerNet):
    def __init__(self):
        super().__init__()

    # 加载路网后
    def afterLoadNet(self):
        # =============== 能执行这里说明是正版key就开启相关功能 ===============
        # (1) 路段编辑-打断路段
        if GlobalVar.action_network_edit_split is not None:
            GlobalVar.action_network_edit_split.setEnabled(True)
        # (2) 仿真数据导出-导出轨迹数据
        GlobalVar.action_simu_export_trajectory.setEnabled(True)
        # (3) 项目配置文件导出-导出选区数据
        if GlobalVar.action_file_export_grid is not None:
            GlobalVar.action_file_export_grid.setEnabled(True)

        # =============== 打印属性信息 ===============
        iface = tessngIFace()
        netiface = iface.netInterface()
        attrs = netiface.netAttrs().otherAttrs()
        print("=" * 66)
        print("Load network! Network attrs:")
        if attrs:
            for k, v in attrs.items():
                print(f"\t{k:<15}:{' '*5}{v}")
        else:
            print("\t(EMPTY)")
        print("=" * 66, "\n")

    # 鼠标点击后触发
    def afterViewMousePressEvent(self, event):
        # (1) 路段编辑-打断路段
        if GlobalVar.is_need_select_network_edit_split:
            GlobalVar.function_network_edit_split(event)
        # (2) 项目配置文件导出-导出选区数据
        if GlobalVar.is_need_select_file_export_grid:
            GlobalVar.function_file_export_grid(event)

    # 控制曲率最小距离
    def ref_curvatureMinDist(self, itemType: int, itemId: int, ref_minDist):
        ref_minDist.value = 0.1
        return True
