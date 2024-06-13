import json

from ..BaseOther2Tessng import BaseOther2Tessng
from .AidaroeNetworkAnalyser import AidaroeNetworkAnalyser


class Aidaroe2Tessng(BaseOther2Tessng):
    """
    params:
        - file_path
    """

    data_source = "Aidaroe"
    pgd_index_create_network = (11, 12)

    def read_data(self, params: dict) -> dict:
        file_path = params["file_path"]
        network_data = json.load(open(file_path, encoding="utf-8"))
        for k, v in network_data.items():
            try:
                network_data[k] = json.loads(v)
            except json.JSONDecodeError:
                pass
        return network_data

    def analyze_data(self, network_data: dict, params: dict) -> dict:
        # 解析数据
        network_analyser = AidaroeNetworkAnalyser()
        analysed_data = network_analyser.analyse_all_data(network_data)
        return analysed_data
