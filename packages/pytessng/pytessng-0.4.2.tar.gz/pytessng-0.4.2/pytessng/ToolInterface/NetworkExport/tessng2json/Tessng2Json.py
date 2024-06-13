import json
from pyproj import Proj

from ..BaseTessng2Other import BaseTessng2Other
from ...public.Line.LineBase import LineBase
from pytessng.Logger import logger
from pytessng.ProgressDialog import ProgressDialogClass as pgd


class Tessng2Json(BaseTessng2Other):
    def save_data(self, data: dict, file_path: str):
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

    def analyze_data(self, netiface, proj_string: str = None):
        network_data = {
            "header": "",
            "name": "",
            "road": [],
            "connector": [],
            "area": [],
            "crosswalk": [],
        }

        # ==================== 1.读取proj ====================
        # 如果有经纬度信息
        projection = None
        if proj_string:
            network_data["header"] = proj_string
            projection = Proj(proj_string)

        # ==================== 2.读取move ====================
        move_distance = netiface.netAttrs().otherAttrs().get("move_distance")
        move = {"x_move": 0, "y_move": 0} if (move_distance is None or "tmerc" in proj_string) else move_distance

        # ==================== 3.读取面域和连接段 ====================
        # 在遍历连接段的时候记录路段的转向类型
        turn_type_mapping = {}

        areas = netiface.allConnectorArea()
        for area in pgd.progress(areas, '连接段数据保存中（1/2）'):
            area_data = {
                "id": area.id(),
                "incommingRoads": [],
                "outgoingRoads": [],
                "connector": [],
                "crosswalk": []
            }

            # 面域边界点
            area_boundary_points = []

            # 保存连接段信息
            for connector in area.allConnector():
                connector_data = {
                    'id': connector.id(),
                    'areaId': area.id(),
                    'predecessor': connector.fromLink().id(),
                    'successor': connector.toLink().id(),
                    'links': []
                }

                area_data["connector"].append(connector_data['id'])
                if connector_data['predecessor'] not in area_data["incommingRoads"]:
                    area_data["incommingRoads"].append(connector_data['predecessor'])
                if connector_data['successor'] not in area_data["outgoingRoads"]:
                    area_data["outgoingRoads"].append(connector_data['successor'])

                # 连接段分车道
                for lane_connector in connector.laneConnectors():
                    lane_connector_data = {
                        'predecessor': lane_connector.fromLane().id(),
                        'predecessorNumber': lane_connector.fromLane().number(),
                        'successor': lane_connector.toLane().id(),
                        'successorNumber': lane_connector.toLane().number(),
                        'center_points_tess': self._qtpoint2list(lane_connector.centerBreakPoint3Ds(), move),
                        'left_points_tess': self._qtpoint2list(lane_connector.leftBreakPoint3Ds(), move),
                        'right_points_tess': self._qtpoint2list(lane_connector.rightBreakPoint3Ds(), move),
                    }
                    lane_connector_data['start_points_tess'] = lane_connector_data['center_points_tess'][0]
                    lane_connector_data['end_points_tess'] = lane_connector_data['center_points_tess'][-1]

                    if proj_string:
                        lane_connector_data['center_points_real'] = self._xy2lonlat(lane_connector_data['center_points_tess'], projection)
                        lane_connector_data['left_points_real'] = self._xy2lonlat(lane_connector_data['left_points_tess'], projection)
                        lane_connector_data['right_points_real'] = self._xy2lonlat(lane_connector_data['right_points_tess'], projection)
                        lane_connector_data['start_points_real'] = lane_connector_data['center_points_real'][0]
                        lane_connector_data['end_points_real'] = lane_connector_data['center_points_real'][-1]

                    lane_connector_data['length'] = self._p2m(lane_connector.length())

                    connector_data['links'].append(lane_connector_data)

                    turn_type = LineBase.calculate_turn_type(lane_connector_data['center_points_tess'])

                    if lane_connector_data['predecessor'] not in turn_type_mapping.keys():
                        turn_type_mapping[lane_connector_data['predecessor']] = []
                    turn_type_mapping[lane_connector_data['predecessor']].append(turn_type)

                    left_points = self._qtpoint2list(lane_connector.leftBreakPoint3Ds(), move)
                    right_points = self._qtpoint2list(lane_connector.rightBreakPoint3Ds(), move)
                    one_lane_points = left_points + right_points[::-1]
                    x, y, z = zip(*one_lane_points)
                    one_lane_points = list(zip(x, y))
                    area_boundary_points.append(one_lane_points)

                network_data['connector'].append(connector_data)

            boundary_points = LineBase.calculate_boundary_points(area_boundary_points)
            if boundary_points:
                area_data["points_tess"] = boundary_points
                if proj_string:
                    area_data["points_real"] = [projection(x, y, inverse=True) for x, y in boundary_points]
            else:
                logger.logger_pytessng.error(f"Failed to calculate boundary points of area {area.id()}!")

            network_data["area"].append(area_data)

        # ==================== 4.读取路段 ====================
        links = netiface.links()
        for link in pgd.progress(links, '路段数据保存中（2/2）'):
            link_data = {}
            link_data["id"] = link.id()
            link_data['points_tess'] = self._qtpoint2list(link.centerBreakPoint3Ds(), move)
            if proj_string:
                link_data['points_real'] = self._xy2lonlat(link_data['points_tess'], projection)
            link_data['bearing'] = LineBase.calculate_angle_with_y_axis(link_data['points_tess'][-2], link_data['points_tess'][-1])
            link_data['lanes'] = []

            # 路段分车道
            for lane in link.lanes():
                lane_data = {
                    'id': lane.id(),
                    'type': lane.actionType(),
                    'center_points_tess': self._qtpoint2list(lane.centerBreakPoint3Ds(), move),
                    'left_points_tess': self._qtpoint2list(lane.leftBreakPoint3Ds(), move),
                    'right_points_tess': self._qtpoint2list(lane.rightBreakPoint3Ds(), move)
                }
                lane_data['start_points_tess'] = lane_data['center_points_tess'][0]
                lane_data['end_points_tess'] = lane_data['center_points_tess'][-1]

                if proj_string:
                    lane_data['center_points_real'] = self._xy2lonlat(lane_data['center_points_tess'], projection)
                    lane_data['left_points_real'] = self._xy2lonlat(lane_data['left_points_tess'], projection)
                    lane_data['right_points_real'] = self._xy2lonlat(lane_data['right_points_tess'], projection)
                    lane_data['start_points_real'] = lane_data['center_points_real'][0]
                    lane_data['end_points_real'] = lane_data['center_points_real'][-1]

                lane_data['length'] = self._p2m(lane.length())
                lane_data['laneNumber'] = lane.number()
                lane_data['turnType'] = list(set(turn_type_mapping.get(lane.id(), [])))
                lane_data['limitSpeed'] = self._p2m(link.limitSpeed())  # km/h

                link_data['lanes'].append(lane_data)

            network_data['road'].append(link_data)

        return network_data


