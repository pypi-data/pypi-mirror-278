from ..BaseNetworkAnalyser import BaseNetworkAnalyser
from pytessng.ProgressDialog import ProgressDialogClass as pgd


class ZhechengNetworkAnalyser(BaseNetworkAnalyser):
    def __init__(self):
        super().__init__()
        self._valid_hour = 10

    def analyse_all_data(self, data: tuple, params: dict = None) -> dict:
        lane_gdf, lane_connector_gdf, accessory_data = data

        # 解析路段
        lanes_data = self.analyse_lanes(lane_gdf)
        # 解析连接段
        laneConnectors_data = self.analyse_laneConnectors(lane_connector_gdf)

        # 解析车辆组成
        vehicleCompositions_data = self.analyse_vehicleCompositions(accessory_data["vehicleCompositions"])
        # 解析车辆输入
        vehicleInputs_data = self.analyse_vehicleInputs(accessory_data["vehicleInputs"])
        # 解析信号灯组及相位
        signalGroups_data = self.analyse_signalGroups(accessory_data["sigs"])
        # 解析信号灯头
        signalHeads_data = self.analyse_signalHeads(accessory_data["signalHeads"])
        # 解析决策点
        decisionPoints_data = self.analyse_decisionPoints(accessory_data["vehicleRoutingDecisionsStatic"])

        return {
            "links": lanes_data,
            "connectors": laneConnectors_data,
            "vehicleCompositions": vehicleCompositions_data,
            "vehicleInputs": vehicleInputs_data,
            "signalGroups": signalGroups_data,
            "signalHeads": signalHeads_data,
            "decisionPoints": decisionPoints_data,
        }

    # # 解析车道
    # def analyse_lanes(self, lane_gdf: gpd.GeoDataFrame) -> dict:
    #     def _update_center_points(links_data: dict) -> None:
    #         xs, ys = [], []
    #         for link in links_data.values():
    #             points = link["link_points"]
    #             xs.extend([p[0] for p in points])
    #             ys.extend([p[1] for p in points])
    #         x_center = (min(xs) + max(xs)) / 2
    #         y_center = (min(ys) + max(ys)) / 2
    #         self.center_point = [x_center, y_center]
    #
    #     lanes_data = {}
    #     for index, lane_data in self.pgd(lane_gdf.iterrows(), "数据读取中（1/9）"):
    #         lane_id = lane_data["id"]
    #         road_id = lane_data["roadId"]
    #         lane_type = lane_data["type"]
    #         width = lane_data["width"]
    #
    #         pass
    #
    #     # links = [
    #     #     Link(
    #     #         id=link_id,
    #     #         points=link_data["link_points"],
    #     #         lanes_width=link_data["lanes_width"],
    #     #         name=link_data["link_name"],
    #     #     )
    #     #     for link_id, link_data in links_data.items()
    #     # ]
    #
    #     return links
    #
    # # 解析车道连接
    # def analyse_laneConnectors(self, laneConnectors_data: gpd.GeoDataFrame) -> dict:
    #     connectors = [
    #         Connector(
    #             from_link_id=connector_id.split("-")[0],
    #             to_link_id=connector_id.split("-")[1],
    #             from_lane_numbers=connector_data["from_lane_numbers"],
    #             to_lane_numbers=connector_data["to_lane_numbers"],
    #         )
    #         for connector_id, connector_data in connectors_data.items()
    #     ]
    #     return connectors

    # 解析车辆组成
    def analyse_vehicleCompositions(self, original_vehicleCompositions_data: dict) -> dict:
        # 解析车辆组成
        vehicleCompositions_data = {}
        for vehicleComposition in pgd.progress(original_vehicleCompositions_data, "车辆组成数据解析中(5/11)"):
            vehicleComposition_id = str(vehicleComposition["id"])
            vehicleCompositions_data[vehicleComposition_id] = {
                compose["vehicleTypeCode"]: compose["ratio"]
                for compose in vehicleComposition["compose"]
            }
        return vehicleCompositions_data

    # 解析车辆输入
    def analyse_vehicleInputs(self, original_vehicleInputs_data: dict) -> dict:
        vehicleInputs_data = {}
        for vehicleInput in pgd.progress(original_vehicleInputs_data, "车辆输入数据解析中(6/11)"):
            vehicleInput_id = str(vehicleInput["id"])
            link_id = str(vehicleInput["roadId"])
            input_data = [
                {
                    "vehicleCompose_id": input_["vehicleComposeId"],
                    "volume": input_["volume"],  # veh
                    "duration": input_["duration"],  # s
                }
                for input_ in vehicleInput["input"]
            ]
            vehicleInputs_data[vehicleInput_id] = {
                "link_id": link_id,
                "input": input_data
            }
        return vehicleInputs_data

    # 解析信号灯组及相位
    def analyse_signalGroups(self, original_signalGroups_data: dict) -> dict:
        signalGroups_data = {}
        for signalGroup in pgd.progress(original_signalGroups_data, "信号灯组及相位数据解析中(7/11)"):
            signalGroup_id = str(signalGroup["id"])
            cycletime = signalGroup["cycletime"]
            phases = [
                {
                    "id": phase["id"],
                    "colorsAndDurations": [
                        {
                            "color": color,
                            "duration": duration,
                        }
                        for color, duration in zip(phase["colors"], phase["durations"])
                    ]
                }
                for phase in signalGroup["phases"]
            ]
            signalGroups_data[signalGroup_id] = {
                "cycletime": cycletime,
                "phases": phases,
                "hour": self._valid_hour,
            }
        return signalGroups_data

    # 解析信号灯头
    def analyse_signalHeads(self, original_signalHeads_data: dict) -> dict:
        signalHeads_data = {}
        for signalHead in pgd.progress(original_signalHeads_data, "信号灯头数据解析中(8/11)"):
            link_id = str(signalHead["lind"])
            dist = signalHead["dist"]
            lane_number = signalHead["fromLaneNumber"]
            to_lane_number = signalHead["toLaneNumber"]
            signalHead_id = str(signalHead["id"])
            signalHeads_data[signalHead_id] = {
                "link_id": str(link_id),
                "dist": float(dist),
                "lane_number": lane_number,
                "to_lane_number": to_lane_number,
                "signalHead_id": signalHead_id,
            }
        return signalHeads_data

    # 解析决策点
    def analyse_decisionPoints(self, original_decisionPoints_data: dict):
        decisionPoints_data = {}
        for decisionPoint in pgd.progress(original_decisionPoints_data, "决策点和决策路径数据解析中(9/11)"):
            decisionPoint_id = str(decisionPoint["id"])
            link_id = str(decisionPoint["roadId"])
            dist = decisionPoint["dist"]
            routings = [
                {
                    "ratio": float(routing["ratio"]),
                    "routing": routing["routings"]
                }
                for routing in decisionPoint["route"]
            ]
            decisionPoints_data[decisionPoint_id] = {
                "link_id": link_id,
                "dist": dist,
                "routings": routings,
                "hour": self._valid_hour,
            }
        return decisionPoints_data
