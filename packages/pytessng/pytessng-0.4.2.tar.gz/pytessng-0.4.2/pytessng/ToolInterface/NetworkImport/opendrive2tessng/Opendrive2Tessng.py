from lxml import etree

from ..BaseOther2Tessng import BaseOther2Tessng
from .OpendriveNetworkAnalyser import OpendriveNetwokAnalyser


class Opendrive2Tessng(BaseOther2Tessng):
    """
    params:
        - file_path
        - step_length
        - lane_types
    """

    data_source = "OpenDrive"

    def read_data(self, params: dict) -> etree._Element:
        file_path = params["file_path"]
        root_node = etree.parse(open(file_path, "r", encoding='utf-8')).getroot()
        return root_node

    def analyze_data(self, network_data: etree._Element, params: dict):
        # 解析数据
        network_analyser = OpendriveNetwokAnalyser()
        temp_data = network_analyser.analyse_all_data(network_data, params)
        return temp_data

    def create_network(self, temp_data) -> (bool, str):
        network, lane_types = temp_data
        error_junction = network.create_network(lane_types, self.netiface)

        if error_junction:
            print("error_junction:", error_junction)

        response = {
            "status": True,
            "message": "创建成功",
        }

        return response
