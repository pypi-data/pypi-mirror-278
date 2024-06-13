from ..BaseOther2Tessng import BaseOther2Tessng
from .OsmNetworkReader import OSMNetworkReader
from .OsmNetworkAnalyser import OsmNetwokAnalyser


class Osm2Tessng(BaseOther2Tessng):
    """
    params:
        - file_path
        - bounding_box
        - center_point
        - road_class
        - proj_mode
        - save_data_path
    """

    data_source = "OpenStreetMap"
    pgd_index_create_network = (6, 7)

    def __init__(self, netiface, auto_move: bool = True):
        super().__init__(netiface, auto_move)

    def read_data(self, params: dict) -> dict:
        save_file_name = ""  # TODO: 传入非空参数可保存为json文件
        network_data = OSMNetworkReader(params).get_osm_data(save_file_name)
        return network_data

    def analyze_data(self, network_data: dict, params: dict) -> dict:
        # 解析数据
        network_analyser = OsmNetwokAnalyser()
        analysed_data = network_analyser.analyse_all_data(network_data)
        # 更新投影
        self.proj_string = network_analyser.proj_string
        return analysed_data
