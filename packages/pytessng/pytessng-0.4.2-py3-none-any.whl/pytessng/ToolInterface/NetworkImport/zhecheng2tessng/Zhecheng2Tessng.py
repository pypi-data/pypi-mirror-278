import os
import json
import geopandas as gpd

from ..BaseOther2Tessng import BaseOther2Tessng
from .ZhechengNetworkAnalyser import ZhechengNetworkAnalyser
from ..shape2tessng.Shape2Tessng import Shape2Tessng


class Zhecheng2Tessng(BaseOther2Tessng):
    """
    params:
        - folder_path: shp
        - file_path: json
    """

    data_source = "Zhecheng"
    pgd_index_create_network = (10, 11)

    def read_data(self, params: dict) -> tuple:
        folder_path = params["folder_path"]
        file_path = params["file_path"]
        lane_file_name = "lane.shp"
        lane_connector_file_name = "laneConnector.shp"

        # =============== 读取车道文件 ===============
        lane_file_path = os.path.join(folder_path, lane_file_name)
        lane_gdf: gpd.GeoDataFrame = gpd.read_file(lane_file_path)

        # =============== 读取车道连接文件 ===============
        lane_connector_file_path = os.path.join(folder_path, lane_connector_file_name)
        lane_connector_gdf: gpd.GeoDataFrame = gpd.read_file(lane_connector_file_path)


        # =============== 读取附属物Json文件 ===============
        accessory_data: dict = json.load(open(file_path, encoding="utf-8")) if file_path else None

        return lane_gdf, lane_connector_gdf, accessory_data

    def analyze_data(self, network_data: tuple, params: dict) -> dict:
        # 解析数据
        network_analyser = ZhechengNetworkAnalyser()
        analysed_data = network_analyser.analyse_all_data(network_data)
        return analysed_data

    # def before_load(self, netiface, params: dict):
    #     new_params = {
    #         "file_path": params["file_path"],
    #         "is_use_lon_and_lat": True,
    #         "is_use_center_line": True,
    #         "lane_file_name": "lane",
    #         "lane_connector_file_name": "laneConnector",
    #         "proj_mode": "wgs84",
    #     }
    #
    #     Shape2Tessng().load_data(netiface, new_params)
