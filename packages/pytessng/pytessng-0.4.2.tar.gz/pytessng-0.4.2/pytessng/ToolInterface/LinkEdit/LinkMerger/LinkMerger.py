from ..BaseLinkEditor import BaseLinkEditor
from .LinkGroupsSearcher import LinkGroupsSearcher
from ...public.Line.LineBase import LineBase
from ...public.Line.LinkPointsSimplifier import LinkPointsSimplifier
from pytessng.Config import LinkEditConfig
from pytessng.Logger import logger
from pytessng.ProgressDialog import ProgressDialogClass as pgd


class LinkMerger(BaseLinkEditor):
    def __init__(self, netiface):
        super().__init__(netiface)
        self.existing_links_data = self.network_iterator(netiface).get_existing_links_data()
        self.existing_connectorAreas_data = self.network_iterator(netiface).get_connectorAreas_data()

    def edit(self, include_connector: bool = LinkEditConfig.Merger.DEFAULT_INCLUDE_CONNECTOR, simplify_points: bool = LinkEditConfig.Merger.DEFAULT_SIMPLIFY_POINTS) -> None:
        # 得到可以合并的路段的统计
        link_groups: dict = LinkGroupsSearcher(
            self.netiface, self.existing_links_data, self.existing_connectorAreas_data
        ).get_link_groups()

        # 记录新的路段数据
        new_links_data = self.get_new_links_data(link_groups, include_connector, simplify_points)

        # 记录新的连接段数据
        new_connectors_data = self.get_new_connectors_data(link_groups)

        # 创建新的路段和连接段
        network_data = {
            "links": new_links_data,
            "connectors": new_connectors_data
        }
        pgd_index = (4, 6)
        result_create_network = self.network_creator(
            self.netiface,
            pgd_index=pgd_index,
        ).create_network(network_data)

        # 删除旧有路段
        self.delete_links(link_groups, result_create_network["links"])

    # 获取新的路段数据
    def get_new_links_data(self, link_groups, include_connector: bool = True, simplify_points: bool = True) -> list:
        new_links_data = []

        for new_link_id, link_group in pgd.progress(link_groups.items(), "新路段点位计算中（2/6）"):
            # 不需要包括连接段点位
            if not include_connector:
                links = [
                    self.netiface.findLink(link_id)
                    for link_id in link_group
                ]

                points = [
                    point
                    for link in links
                    for point in self._qtpoint2list(link.centerBreakPoint3Ds())
                ]
                lanes_points = [
                    {
                        "left": [
                            point
                            for link in links
                            for point in self._qtpoint2list(link.lanes()[lane_number].leftBreakPoint3Ds())
                        ],
                        "center": [
                            point
                            for link in links
                            for point in self._qtpoint2list(link.lanes()[lane_number].centerBreakPoint3Ds())
                        ],
                        "right": [
                            point
                            for link in links
                            for point in self._qtpoint2list(link.lanes()[lane_number].rightBreakPoint3Ds())
                        ],
                    }
                    for lane_number in range(len(links[0].lanes()))
                ]
            # 需要连接段点位
            else:
                links = []
                for index in range(1, len(link_group)):
                    last_link_id = link_group[index - 1]
                    link_id = link_group[index]
                    if index == 1:
                        link = self.netiface.findLink(last_link_id)
                        links.append(link)

                    connector = self.netiface.findConnectorByLinkIds(last_link_id, link_id)
                    links.append(connector)
                    link = self.netiface.findLink(link_id)
                    links.append(link)

                points = []
                lanes_points = [
                    {
                        "left": [],
                        "center": [],
                        "right": [],
                    }
                    for _ in range(len(links[0].lanes()))
                ]
                for road in links:
                    # 车道点位
                    lanes = road.lanes() if road.isLink() else road.laneConnectors()
                    temp_points = []
                    for index, lane in enumerate(lanes):
                        left_points = self._qtpoint2list(lane.leftBreakPoint3Ds())
                        center_points = self._qtpoint2list(lane.centerBreakPoint3Ds())
                        right_points = self._qtpoint2list(lane.rightBreakPoint3Ds())
                        lanes_points[index]["left"].extend(left_points)
                        lanes_points[index]["center"].extend(center_points)
                        lanes_points[index]["right"].extend(right_points)
                        temp_points.append([left_points, right_points])

                    # 路段点位
                    if road.isLink():
                        points_ = self._qtpoint2list(road.centerBreakPoint3Ds())
                    # 连接段的根据左右边线计算
                    else:
                        right_points = temp_points[0][1]
                        left_points = temp_points[-1][0]
                        points_ = LineBase.merge_two_lines(left_points, right_points)
                    points.extend(points_)

            # 点位简化
            if simplify_points:
                points, lanes_points = LinkPointsSimplifier.simplify_link(points, lanes_points, 0.3)

            # 车道类型
            lanes_type = [
                lane.actionType()
                for lane in links[0].lanes()
            ]
            # 路段限速
            limit_speed = self._p2m(links[0].limitSpeed())
            # 路段名称
            name = "-".join(set([
                link.name()
                for link in links
                if "-" not in link.name()
            ]))

            new_links_data.append({
                "id": new_link_id,
                "points": points,
                "lanes_points": lanes_points,
                "lanes_type": lanes_type,
                "limit_speed": limit_speed,
                "name": name,
            })

        return new_links_data

    # 获取新的连接段数据
    def get_new_connectors_data(self, link_groups: dict) -> list:
        new_connectors_data = []
        new_link_id_mapping = {
            link_id: new_link_id
            for new_link_id, link_group in link_groups.items()
            for link_id in link_group
        }

        for new_link_id, link_group in pgd.progress(link_groups.items(), "新连接段记录中（3/6）"):
            # 首路段上游的连接段
            start_link_id = link_group[0]
            last_link_ids = self.existing_links_data[start_link_id]["last_link_ids"]
            for last_link_id in last_link_ids:
                connector = self.netiface.findConnectorByLinkIds(last_link_id, start_link_id)
                last_link_id = new_link_id_mapping.get(last_link_id, last_link_id)
                from_lane_numbers = sorted([
                    laneConnector.fromLane().number() + 1
                    for laneConnector in connector.laneConnectors()
                ])
                to_lane_numbers = sorted([
                    laneConnector.toLane().number() + 1
                    for laneConnector in connector.laneConnectors()
                ])
                connectors_data = {
                    "from_link_id": last_link_id,
                    "to_link_id": new_link_id,
                    "from_lane_numbers": from_lane_numbers,
                    "to_lane_numbers": to_lane_numbers,
                }
                if connectors_data not in new_connectors_data:
                    new_connectors_data.append(connectors_data)

            # 末路段上游的连接段
            end_link_id = link_group[-1]
            next_link_ids = self.existing_links_data[end_link_id]["next_link_ids"]
            for next_link_id in next_link_ids:
                connector = self.netiface.findConnectorByLinkIds(end_link_id, next_link_id)
                next_link_id = new_link_id_mapping.get(next_link_id, next_link_id)
                from_lane_numbers = sorted(
                    [laneConnector.fromLane().number() + 1
                     for laneConnector in connector.laneConnectors()
                     ])
                to_lane_numbers = sorted(
                    [laneConnector.toLane().number() + 1
                     for laneConnector in connector.laneConnectors()
                     ])
                connectors_data = {
                    "from_link_id": new_link_id,
                    "to_link_id": next_link_id,
                    "from_lane_numbers": from_lane_numbers,
                    "to_lane_numbers": to_lane_numbers,
                }
                if connectors_data not in new_connectors_data:
                    new_connectors_data.append(connectors_data)

        return new_connectors_data

    # 删除旧有路段
    def delete_links(self, link_groups: dict, result_create_links: dict) -> None:
        messages = []
        for new_link_id, link_group in pgd.progress(link_groups.items(), "原有路段及连接段删除中（6/6）"):
            create_link_id = result_create_links[str(new_link_id)]

            # 如果创建成功了，删除原有路段
            if create_link_id:
                for link_id in link_group:
                    link = self.netiface.findLink(link_id)
                    if link is not None:
                        self.netiface.removeLink(link)
                messages.append(f"{link_group} -> [{create_link_id}]")
            else:
                messages.append(f"{link_group} failed to be merged")

            logger.logger_pytessng.info("Merge message:\n\t" + "\n\t".join(messages))
