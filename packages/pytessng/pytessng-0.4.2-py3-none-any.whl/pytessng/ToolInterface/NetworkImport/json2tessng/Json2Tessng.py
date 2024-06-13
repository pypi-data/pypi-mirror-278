import json

from ..BaseOther2Tessng import BaseOther2Tessng
from pytessng.ProgressDialog import ProgressDialogClass as pgd


class Json2Tessng(BaseOther2Tessng):
    """
    params:
        - file_path
    """

    data_source = "Json"
    pgd_index_create_network = (3, 4)

    def read_data(self, params: dict) -> dict:
        file_path = params["file_path"]
        # 获取文件后缀
        try:
            network_data = json.load(open(file_path, encoding="utf-8"))
        except:
            network_data = json.load(open(file_path, encoding="gbk"))
        return network_data

    def analyze_data(self, network_data: dict, params: dict) -> dict:
        standard_links_data, standard_connectors_data = [], []

        lanes_mapping = {}

        # ==================== 路段 ====================
        for link_data in pgd.progress(network_data["road"], '路段数据解析中（1/4）'):
            id = link_data["id"]
            points = link_data["points_tess"]
            for index, lane in enumerate(link_data["lanes"], start=1):
                lanes_mapping[lane["id"]] = index
            lanes_points = [
                {
                    "left": lane["left_points_tess"],
                    "center": lane["center_points_tess"],
                    "right": lane["right_points_tess"],
                }
                for lane in link_data["lanes"]
            ]
            lanes_type = [lane["type"] for lane in link_data["lanes"]]
            standard_link_data = dict(
                id=id,
                points=points,
                lanes_points=lanes_points,
                lanes_type=lanes_type,
            )
            standard_links_data.append(standard_link_data)

        # ==================== 连接段 ====================
        for connector_data in pgd.progress(network_data["connector"], '连接段数据解析中（2/4）'):
            from_link_id = connector_data["predecessor"]
            to_link_id = connector_data["successor"]
            from_lane_numbers = [lanes_mapping[lane["predecessor"]] for lane in connector_data["links"]]
            to_lane_numbers = [lanes_mapping[lane["successor"]] for lane in connector_data["links"]]
            # TODO 暂不考虑连接段点位

            standard_connector_data = dict(
                from_link_id=from_link_id,
                to_link_id=to_link_id,
                from_lane_numbers=from_lane_numbers,
                to_lane_numbers=to_lane_numbers,
            )
            standard_connectors_data.append(standard_connector_data)

        # ==================== 投影 ====================
        self.proj_string = network_data.get("header")

        return {
            "links": standard_links_data,
            "connectors": standard_connectors_data,
        }
