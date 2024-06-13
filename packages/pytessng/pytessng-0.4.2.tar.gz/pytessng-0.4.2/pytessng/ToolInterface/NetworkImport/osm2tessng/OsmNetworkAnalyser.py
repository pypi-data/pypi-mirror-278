import math
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import LineString
from shapely.geometry import Point
from scipy.spatial import KDTree

from ..BaseNetworkAnalyser import BaseNetworkAnalyser
from pytessng.Config import NetworkImportConfig
from pytessng.Logger import logger
from pytessng.ProgressDialog import ProgressDialogClass as pgd


# 节点类
class Node:
    def __init__(self, id_: str, loc: tuple, adjacent_links: list):
        self.id = id_
        self.loc = loc
        self.adjacent_links = adjacent_links


# 路段类
class Link:
    """
    主要有几个功能点：
        (1) 获取头一段的角度(start_angle)和尾一段的角度(end_angle)；
        (2) 按距离切分(cut)；
        (3) 生成平行路段(shift)；
        (4) 绘制(draw)。
    """

    def __init__(self, id_: str, name: str, _type: str, line: LineString, start_node_id: str, end_node_id: str,
                 is_oneway: bool, lane_count: int):
        self.id = id_
        self.name = name
        self.type = _type

        self.line = line
        self.length = self.line.length

        self.start_node_id = start_node_id
        self.end_node_id = end_node_id
        self.is_oneway = is_oneway
        self.lane_count = lane_count

        # 头一段的角度
        self._start_angle = None
        # 尾一段的角度
        self._end_angle = None

    ###########################################################################

    # 计算线段与x正轴的逆时针夹角(-180≤angle≤180)
    @staticmethod
    def calc_line_angle(first_point: tuple, second_point: tuple) -> float:
        x1, y1 = first_point
        x2, y2 = second_point
        dx = x2 - x1
        dy = y2 - y1
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)
        # 确保角度在-180到180
        angle_deg = (angle_deg + 180) % 360 - 180
        return angle_deg

    # 获取一条线开始段或结束段的角度(-180≤angle≤180)
    @staticmethod
    def get_specific_angle(line: LineString, loc: str) -> float:
        if loc == "start":
            v1, v2 = 0.1, 0.2
        elif loc == "end":
            v1, v2 = line.length - 0.2, line.length - 0.1
        else:
            raise Exception("No this mode.")
        try:
            # 获取点
            p1 = line.interpolate(v1)
            p2 = line.interpolate(v2)
            # 获取坐标
            point1 = (p1.x, p1.y)
            point2 = (p2.x, p2.y)
        except:
            raise Exception("Failed to obtain points.")
        # 计算角度
        angle = Link.calc_line_angle(point1, point2)
        return angle

    # 头一段的角度
    @property
    def start_angle(self):
        if self._start_angle is None:
            self._start_angle = Link.get_specific_angle(self.line, "start")
        return self._start_angle

    # 尾一段的角度
    @property
    def end_angle(self):
        if self._end_angle is None:
            self._end_angle = Link.get_specific_angle(self.line, "end")
        return self._end_angle

    ###########################################################################

    # 按距离切分
    def cut(self, distance: int, save: str) -> None:
        line = self.line

        if distance <= 1:
            logger.logger_pytessng.debug(
                f"OpenStreetMap: Cutting distance {distance} is too short for the line{self.id}'s length {line.length}!")
            distance = 1
        # 防止溢出
        elif distance >= line.length - 1:
            logger.logger_pytessng.debug(
                f"OpenStreetMap: Cutting distance {distance} is too long for the line{self.id}'s length {line.length}!")
            distance = line.length - 1

        coords = list(line.coords)
        for i, point in enumerate(coords):
            pd = line.project(Point(point))
            if pd == distance:
                split_lines = [LineString(coords[:i + 1]), LineString(coords[i:])]
                break
            elif pd > distance:
                cp = line.interpolate(distance)
                split_lines = [LineString(coords[:i] + [(cp.x, cp.y)]), LineString([(cp.x, cp.y)] + coords[i:])]
                break

        # 保存哪一段
        if save == "frist":
            self.line = split_lines[0]
        elif save == "second":
            self.line = split_lines[1]
        else:
            raise Exception("Invalid save mode!")
        # 更新长度
        self.length = self.line.length

    ###########################################################################

    # 给两个点算ABC
    @staticmethod
    def calc_line_coefficients(first_point: tuple, second_point: tuple) -> (float, float, float):
        x1, y1 = first_point
        x2, y2 = second_point
        # 处理垂直线，斜率不存在
        if x1 == x2:
            A, B, C = 1, 0, -x1
        else:
            # 计算斜率
            m = (y2 - y1) / (x2 - x1)
            # 计算截距
            b = y1 - m * x1
            # 转换为Ax + By + C = 0的形式
            A, B, C = -m, 1, -b
        return A, B, C

    # 计算两直线交点
    @staticmethod
    def find_lines_intersection(first_line_coeff: tuple, second_line_coeff: tuple, point: tuple) -> (float, float):
        A1, B1, C1 = first_line_coeff
        A2, B2, C2 = second_line_coeff
        # 计算分母
        denominator = A1 * B2 - A2 * B1
        # 如果分母接近零，说明直线平行或重合
        if abs(denominator) < 1e-6:
            x, y = point
        else:
            # 计算交点坐标
            x = (B1 * C2 - B2 * C1) / denominator
            y = (A2 * C1 - A1 * C2) / denominator
        return x, y

    # 计算向[左]偏移一定距离的线段
    @staticmethod
    def get_left_shift_line(first_point: tuple, second_point: tuple, width: float) -> (tuple, tuple):
        # 获取坐标
        x1, y1 = first_point
        x2, y2 = second_point
        # 计算法向量的分量
        nx = -(y2 - y1)
        ny = x2 - x1
        # 计算法向量的长度
        length = np.sqrt(nx ** 2 + ny ** 2)
        # 计算单位法向量
        ux = nx / length
        uy = ny / length
        # 计算偏移后的点坐标
        new_first_point = (x1 + ux * width, y1 + uy * width)
        new_second_point = (x2 + ux * width, y2 + uy * width)
        return new_first_point, new_second_point

    # 计算向[左]偏移一定距离的多义线
    @staticmethod
    def get_left_shift_lines(line: list, width: float) -> list:
        if len(line) < 2:
            raise Exception("Too less points count!")
        shift_line = []
        for i in range(1, len(line)):
            # 获取偏移线段
            new_first_point, new_second_point = Link.get_left_shift_line(line[i - 1], line[i], width)
            # 计算多义线偏移
            if i == 1:
                shift_line.append(new_first_point)
                line_coeff = Link.calc_line_coefficients(new_first_point, new_second_point)
            else:
                last_line_coeff = line_coeff
                line_coeff = Link.calc_line_coefficients(new_first_point, new_second_point)
                new_point = Link.find_lines_intersection(last_line_coeff, line_coeff, new_first_point)
                shift_line.append(new_point)
            if i == len(line) - 1:
                shift_line.append(new_second_point)
        return shift_line

    # 根据车道数横向偏移
    @staticmethod
    def get_offset_width(lane_count=3) -> float:
        offset_x = NetworkImportConfig.OSM.DEFAULT_LANE_WIDTH * lane_count / 2
        return offset_x

    # 计算平行线
    def shift(self, width: float = None):
        if not width:
            width = Link.get_offset_width(self.lane_count)

        line = list(self.line.coords)
        # 确保折线至少有两个点
        if len(line) < 2:
            raise ValueError("A polyline requires at least two points !")

        # 两侧偏移
        left_line = LineString(Link.get_left_shift_lines(line, width)[::-1])
        right_line = LineString(Link.get_left_shift_lines(line, -width))

        # 创建两个对象
        left_link = Link(f"L[{self.id}]", self.name, self.type, left_line, self.end_node_id, self.start_node_id, True,
                         self.lane_count)
        right_link = Link(f"R[{self.id}]", self.name, self.type, right_line, self.start_node_id, self.end_node_id,
                          True, self.lane_count)

        return left_link, right_link

    ###########################################################################

    # 绘制路段
    def draw(self):
        line = list(self.line.coords)
        xs, ys = [], []
        for x, y in line:
            xs.append(x)
            ys.append(y)
        plt.plot(xs, ys)
        plt.axis("equal")


# 连接段类
class Connector:
    def __init__(self, from_link_id: str, to_link_id: str, from_lane_number: list, to_lane_number: list):
        self.from_link_id = from_link_id
        self.to_link_id = to_link_id
        self.from_lane_number = from_lane_number  # start from one
        self.to_lane_number = to_lane_number  # start from one


# 转向类
class Turn:
    def __init__(self, from_link: Link, to_links: dict):
        self.from_link = from_link
        self._to_links = to_links

        self._left = self._to_links["left"]
        self._straight = self._to_links["straight"]
        self._right = self._to_links["right"]

        self.conns = []
        # 有没有连接问题
        self.error = False

        # 创建转向
        self._init_turn()

    def _init_turn(self):
        left_count = len(self._left)
        straight_count = len(self._straight)
        right_count = len(self._right)

        if left_count > 1 or straight_count > 1 or right_count > 1:
            logger.logger_pytessng.debug(
                f"OpenStreetMap: Too much turn as [left]-[{left_count}] $ [straight]-[{straight_count}] $ [right]-[{right_count}].")
            self.error = True

        self._init_right()
        self._init_left()
        self._init_straight()

    # 右转
    def _init_right(self):
        left = self._left
        straight = self._straight
        right = self._right
        from_link_id = self.from_link.id
        from_lane_count = self.from_link.lane_count

        # 只有右转
        if not left and not straight and right:
            # TODO 没有考虑进出车道不平衡的时候
            for to_link_id, to_link in right.items():
                to_lane_count = to_link.lane_count
                laneCount = min(from_lane_count, to_lane_count)
                from_lane_number = [i + 1 for i in range(laneCount)]
                to_lane_number = [i + 1 for i in range(laneCount)]
                conn = Connector(from_link_id, to_link_id, from_lane_number, to_lane_number)
                self.conns.append(conn)
        # 不是只有右转
        else:
            # 最右侧连最右侧
            for to_link_id, to_link in right.items():
                from_lane_number = [1]
                to_lane_number = [1]
                conn = Connector(from_link_id, to_link_id, from_lane_number, to_lane_number)
                self.conns.append(conn)

    # 左转
    def _init_left(self):
        left = self._left
        straight = self._straight
        right = self._right
        from_link_id = self.from_link.id
        from_lane_count = self.from_link.lane_count

        # 只有左转
        if left and not straight and not right:
            # TODO 没有考虑进出车道不平衡的时候
            for to_link_id, to_link in left.items():
                to_lane_count = to_link.lane_count
                laneCount = min(from_lane_count, to_lane_count)
                from_lane_number = [i + 1 for i in range(laneCount)]
                to_lane_number = [i + 1 for i in range(laneCount)]
                conn = Connector(from_link_id, to_link_id, from_lane_number, to_lane_number)
                self.conns.append(conn)
        # 不是只有左转
        else:
            # 最左侧连最左侧
            for to_link_id, to_link in left.items():
                to_lane_count = to_link.lane_count
                from_lane_number = [from_lane_count]
                to_lane_number = [to_lane_count]
                conn = Connector(from_link_id, to_link_id, from_lane_number, to_lane_number)
                self.conns.append(conn)

    # 直行
    def _init_straight(self):
        left = self._left
        straight = self._straight
        right = self._right
        from_link_id = self.from_link.id
        from_lane_count = self.from_link.lane_count

        # 没有左转有直行
        if not left and straight:
            # TODO 没有考虑进出车道不平衡的时候
            for to_link_id, to_link in straight.items():
                to_lane_count = to_link.lane_count
                laneCount = min(from_lane_count, to_lane_count)
                from_lane_number = [i + 1 for i in range(laneCount)]
                to_lane_number = [i + 1 for i in range(laneCount)]
                conn = Connector(from_link_id, to_link_id, from_lane_number, to_lane_number)
                self.conns.append(conn)
        # 只有一条车道
        elif from_lane_count == 1:
            for to_link_id, to_link in straight.items():
                to_lane_count = to_link.lane_count
                from_lane_number = [1 for _ in range(to_lane_count)]
                to_lane_number = [i + 1 for i in range(to_lane_count)]
                conn = Connector(from_link_id, to_link_id, from_lane_number, to_lane_number)
                self.conns.append(conn)
        # 有左转有直行
        else:
            for to_link_id, to_link in straight.items():
                to_lane_count = to_link.lane_count
                laneCount = min(from_lane_count, to_lane_count)
                # 给左转留地方
                from_lane_number = [i + 1 for i in range(laneCount) if i + 1 != laneCount]
                to_lane_number = [i + 1 for i in range(laneCount) if i + 1 != laneCount]
                conn = Connector(from_link_id, to_link_id, from_lane_number, to_lane_number)
                self.conns.append(conn)


# 交叉口类
class Intersection:
    """
    主要是两个步骤：
        (1) 处理路段(_handle_links)；
        (2) 处理连接段(_handle_conns).
    可以绘制交叉口包含路段(draw).
    """

    def __init__(self, nodes: dict, links: dict):
        self.nodes = nodes
        self.links = links

        # _init_links的输出
        # 维持与路网数据的一致性
        self.update_node = {}
        self.update_link = {
            "insert": {},  # 增加
            "update": {},  # 更新
            "delete": {},  # 删除
        }

        # _init_conns的输出
        # 交叉口连接
        self.conns = []
        # 问题转向
        self.error_turn_list = []

        # 创建交叉口
        self._init_intersection()

    # 创建交叉口
    def _init_intersection(self):
        if not self.nodes or not self.links:
            logger.logger_pytessng.warning("Empty intersection data !")
            return

        # 处理路段
        self._init_links()
        # 处理连接段
        self._init_conns()

    ###########################################################################

    # 裁剪长度
    def _get_offset_y(self, node_num):
        if node_num == 1:
            offset_oneway = 15
            offset_twoway = 15
        elif node_num == 2:
            offset_oneway = 15
            offset_twoway = 10
        elif node_num in [3, 4]:
            offset_oneway = 15
            offset_twoway = 15
        else:
            raise Exception("Too much node !")
        return offset_oneway, offset_twoway

    # 裁剪边
    def _cut_link(self, link):
        offset_oneway, offset_twoway = self._get_offset_y(len(self.nodes))
        if link.is_oneway:
            # 出边
            if link.start_node_id in self.nodes:
                link.cut(offset_oneway, "second")
            # 入边
            elif link.end_node_id in self.nodes:
                link.cut(link.length - offset_oneway, "frist")
        else:
            # 出边
            if link.start_node_id in self.nodes:
                link.cut(offset_twoway, "second")
            # 入边
            elif link.end_node_id in self.nodes:
                link.cut(link.length - offset_twoway, "frist")
        return link

    # 裁剪和复制边
    def _init_links(self):
        links = self.links.copy()

        for link_id, link in links.items():
            # 如果是交叉口内部的边就删掉
            if link.start_node_id in self.nodes and link.end_node_id in self.nodes:
                # 自己要更新
                self.links.pop(link_id)
                # 路网要更新
                self.update_link["delete"][link_id] = True
                self.update_node[link_id] = []
            else:
                # 裁剪边
                link = self._cut_link(link)
                # 单向边
                if link.is_oneway:
                    # 自己要更新
                    self.links[link_id] = link
                    # 路网要更新
                    self.update_link["update"][link_id] = link
                # 双向边
                else:
                    link1, link2 = link.shift()
                    # 自己要更新
                    self.links.pop(link_id)
                    self.links[link1.id] = link1
                    self.links[link2.id] = link2
                    # 路网要更新
                    self.update_link["delete"][link_id] = True
                    self.update_link["insert"][link1.id] = link1
                    self.update_link["insert"][link2.id] = link2
                    self.update_node[link_id] = [link1.id, link2.id]

    ###########################################################################

    # 得到路段一圈的顺序
    def _get_link_order(self, ):
        cut_length = 5
        points = {}
        for link_id, link in self.links.items():
            if link.start_node_id in self.nodes:
                length = cut_length
            else:
                length = max(link.length - cut_length, 0)
            p = link.line.interpolate(length)
            points[link_id] = (p.x, p.y)

        # 计算交叉口中心位置
        center_x = np.mean([p[0] for p in points.values()])
        center_y = np.mean([p[1] for p in points.values()])
        center_point = (center_x, center_y)

        # 时针顺序
        link_order = []
        for link_id, point in points.items():
            angle = Link.calc_line_angle(center_point, point)
            link_order.append([link_id, angle])
        link_order = sorted(link_order, key=lambda x: x[1])
        link_order = [link_id for link_id, _ in link_order]
        return link_order

    # 判断谁进谁出
    def _get_link_inout(self, link_order):
        link_inout = {"in": [], "out": []}
        for link_id in link_order:
            link = self.links[link_id]
            if link.start_node_id in self.nodes:
                link_inout["out"].append([link_id, link.start_angle])
            else:
                link_inout["in"].append([link_id, link.end_angle])
        return link_inout

    # 判断左直右
    def _get_to_links(self, link_inout):
        to_links = {}
        for link_id, angle_1 in link_inout["in"]:
            turn = {"left": {}, "straight": {}, "right": {}}
            for link_id_2, angle_2 in link_inout["out"]:
                link = self.links[link_id_2]
                # 将结果限制在-180~180
                diff_angle = (angle_2 - angle_1 + 180) % 360 - 180
                # 直行
                if -45 <= diff_angle <= 45:
                    turn["straight"][link_id_2] = link
                # 左转
                elif 45 < diff_angle < 135:
                    turn["left"][link_id_2] = link
                # 右转
                elif -135 < diff_angle < -45:
                    turn["right"][link_id_2] = link
            to_links[link_id] = turn
        return to_links

    # 进行交叉口连接
    def _init_conns(self, ):
        # 时针顺序
        link_order = self._get_link_order()
        # 判断进出关系
        link_inout = self._get_link_inout(link_order)
        # 判断左直右
        to_links = self._get_to_links(link_inout)

        # 连接
        for link_id in to_links:
            from_link = self.links[link_id]  # Link
            single_to_links = to_links[link_id]  # dict(turn_type: Link)
            # 转向对象
            turn = Turn(from_link, single_to_links)
            self.conns.extend(turn.conns)
            # 如果有问题
            if turn.error:
                self.error_turn_list.append(turn)

    ###########################################################################

    # 绘制交叉口包含路段
    def draw(self):
        links = self.links
        for link in links.values():
            link.draw()


# 路网数据类
class NetworkData:
    def __init__(self, edges_info: dict, nodes_info: dict, other_info: dict):
        self._links = edges_info
        self._nodes = nodes_info
        self.network_other = other_info
        self.network_links = {}
        self.network_nodes = {}

        self._init_()

    def _init_(self):
        if not self._links or not self._nodes:
            logger.logger_pytessng.warning("Empty network data!")
            return

        # 转换点
        for node_id, node in pgd.progress(self._nodes.items(), '数据解析中（3/7）'):
            node_id = str(node_id)
            loc = node["loc"]
            adjacent_links = [str(link_id) for link_id in node["adjacent_links"]]
            self.network_nodes[node_id] = Node(node_id, loc, adjacent_links)

        # 转换边
        for link_id, link in pgd.progress(self._links.items(), '数据解析中（4/7）'):
            link_id = str(link_id)
            name = link.get("name", "")
            _type = link["highway"]
            line = LineString(link["geometry"])
            start_node_id = str(link["start_node_id"])
            end_node_id = str(link["end_node_id"])
            is_oneway = link["is_oneway"]
            lane_count = link["lane_count"]
            self.network_links[link_id] = Link(link_id, name, _type, line, start_node_id, end_node_id, is_oneway,
                                               lane_count)


# 路网类
class Network(NetworkData):
    def __init__(self, edges_info: dict, nodes_info: dict, other_info: dict):
        super().__init__(edges_info, nodes_info, other_info)
        # 连接段数据
        self.network_conns = []

        # 交叉口对象
        self.intersection_id = 0
        self.intersections = {}

        # 问题路段编号
        self.error_link_list = {"type1": [], "type2": []}

        # 创建路网
        self._init_network()

    # 创建路网
    def _init_network(self):
        if not self.network_nodes or not self.network_links:
            return

        # 一、连接路段
        self._connect_links()

        # 二、定位交叉口
        group = self._find_closer_points(30)

        # 三、创建交叉口对象
        for nodes_id in pgd.progress(group.values(), '数据解析中（5/7）'):
            if len(nodes_id) <= 4:
                try:
                    error_turn_list = self._init_intersection(nodes_id)
                    # 转向有问题
                    self._record_error("type1", error_turn_list)
                except:
                    self._record_error("type2", nodes_id)
            else:
                # 路口的点太多
                self._record_error("type2", nodes_id)

        # 四、双向边复制为单向复制边
        self._copy_links()

    ###########################################################################

    # 一条路的中间连起来
    def _connect_links(self):
        network_nodes = self.network_nodes.copy()

        for node_id, node in network_nodes.items():
            neighbor_id = node.adjacent_links
            neighbor_count = len(neighbor_id)

            # 只处理度为2的道路
            if neighbor_count != 2:
                continue

            link_id_1 = neighbor_id[0]
            link_id_2 = neighbor_id[1]
            link1 = self.network_links[link_id_1]
            link2 = self.network_links[link_id_2]

            # 单双属性要一样
            if link1.is_oneway != link2.is_oneway:
                logger.logger_pytessng.debug(
                    f"OpenStreetMap: The is_oneway of link{link_id_1} is different from that of link{link_id_2}.")
                continue

            # 获取道路角度
            if link1.start_node_id == node_id:
                angle1 = link1.start_angle
            else:
                angle1 = link1.end_angle
            if link2.start_node_id == node_id:
                angle2 = link2.start_angle
            else:
                angle2 = link2.end_angle

            # 计算角度差(-180~180)
            diff_angle = (angle2 - angle1 + 180) % 360 - 180

            # 不在一条线上不处理
            if not (-10 < diff_angle < 10 or diff_angle < -170 or diff_angle > 170):
                continue

            # 如果两段的车道数不一样
            if link1.lane_count != link2.lane_count:
                logger.logger_pytessng.debug(
                    f"OpenStreetMap: The lane count of link[{link_id_1}] ({link1.lane_count}) is different from that of link[{link_id_2}] ({link2.lane_count}).")
                lane_count = max(link1.lane_count, link2.lane_count)
            else:
                lane_count = link1.lane_count

            # →o→
            if link1.end_node_id == node_id and link2.start_node_id == node_id:
                start_node_id = link1.start_node_id
                end_node_id = link2.end_node_id
                new_line = LineString(list(link1.line.coords) + list(link2.line.coords)[1:])
                start_link_id = link_id_1
                end_link_id = link_id_2
            # →o←
            elif link1.end_node_id == node_id and link2.end_node_id == node_id:
                start_node_id = link1.start_node_id
                end_node_id = link2.start_node_id
                new_line = LineString(list(link1.line.coords)[:-1] + list(link2.line.coords)[::-1])
                start_link_id = link_id_1
                end_link_id = link_id_2
            # ←o←
            elif link1.start_node_id == node_id and link2.end_node_id == node_id:
                start_node_id = link2.start_node_id
                end_node_id = link1.end_node_id
                new_line = LineString(list(link2.line.coords) + list(link1.line.coords)[1:])
                start_link_id = link_id_2
                end_link_id = link_id_1
            # ←o→
            elif link1.start_node_id == node_id and link2.start_node_id == node_id:
                start_node_id = link1.end_node_id
                end_node_id = link2.end_node_id
                new_line = LineString(list(link1.line.coords)[::-1] + list(link2.line.coords)[1:])
                start_link_id = link_id_1
                end_link_id = link_id_2
            else:
                raise "123"

            # 处理边
            # ——删旧边
            for id_ in neighbor_id:
                self.network_links.pop(id_)
            # ——加新边
            new_link_id = f"{link_id_1},{link_id_2}"
            new_link_name = ",".join(set(link1.name.split(",") + link2.name.split(",")))
            self.network_links[new_link_id] = Link(new_link_id, new_link_name, link1.type, new_line, start_node_id,
                                                   end_node_id, link1.is_oneway, lane_count)

            # 处理点
            # ——删旧点
            self.network_nodes.pop(node_id)
            # ——加新点
            self.network_nodes[start_node_id].adjacent_links.remove(start_link_id)
            self.network_nodes[end_node_id].adjacent_links.remove(end_link_id)
            self.network_nodes[start_node_id].adjacent_links.append(new_link_id)
            self.network_nodes[end_node_id].adjacent_links.append(new_link_id)

    ###########################################################################

    # 给定距离，搜索在该距离内的点集
    def _find_closer_points(self, max_distance: float) -> dict:
        # 只找度大于2的点
        nodes_id = []
        nodes = []
        for node_id, node in self.network_nodes.items():
            if len(node.adjacent_links) >= 2:
                nodes_id.append(node_id)
                nodes.append(node.loc)

        # 树算法
        if len(nodes) >= 2:
            kdtree = KDTree(nodes, leafsize=10)
            pairs = kdtree.query_pairs(max_distance)
        else:
            pairs = []

        # 点分组
        group = {}
        group_id = 0
        for pair in pairs:
            node1_id = nodes_id[pair[0]]
            node2_id = nodes_id[pair[1]]
            if node1_id not in group and node2_id not in group:
                group[node1_id] = group_id
                group[node2_id] = group_id
                group_id += 1
            elif node1_id in group and node2_id not in group:
                group[node2_id] = group[node1_id]
            elif node1_id not in group and node2_id in group:
                group[node1_id] = group[node2_id]
            elif node1_id in group and node2_id in group:
                if group[node2_id] != group[node1_id]:
                    for k, v in group.items():
                        if v == group[node2_id]:
                            group[k] = group[node1_id]

        # 查缺补漏，只有一个点的交叉口
        for node_id in nodes_id:
            if node_id not in group:
                group[node_id] = group_id
                group_id += 1

        new_group = {}
        for node_id, group_id in group.items():
            if group_id not in new_group:
                new_group[group_id] = []
            new_group[group_id].append(node_id)

        return new_group

    ###########################################################################

    # 给node_id，搜索相邻link_id
    def _find_involved_elements(self, nodes_id: list) -> (dict, dict):
        links_id = set()
        for node_id in nodes_id:
            links_id.update(self.network_nodes[node_id].adjacent_links)
        # 获取一个交叉口相关的点和边
        nodes = {node_id: self.network_nodes[node_id] for node_id in nodes_id}
        links = {link_id: self.network_links[link_id] for link_id in links_id}
        return nodes, links

    def _init_intersection(self, nodes_id: list):
        nodes, links = self._find_involved_elements(nodes_id)

        # 初始化交叉口对象
        intersection = Intersection(nodes, links)

        # 获取路网更新信息
        update_link = intersection.update_link
        update_node = intersection.update_node

        # 更新节点
        for old_link_id, new_links_id in update_node.items():
            nodes_id = [
                self.network_links[old_link_id].start_node_id,
                self.network_links[old_link_id].end_node_id
            ]
            for node_id in nodes_id:
                # 删
                self.network_nodes[node_id].adjacent_links.remove(old_link_id)
                # 增
                self.network_nodes[node_id].adjacent_links.extend(new_links_id)

        # 更新路段
        # 删
        for link_id in update_link["delete"]:
            self.network_links.pop(link_id)
        # 改
        for link_id, link in update_link["update"].items():
            self.network_links[link_id] = link
        # 增
        for link_id, link in update_link["insert"].items():
            self.network_links[link_id] = link

        # 获取交叉口连接
        conns = intersection.conns
        self.network_conns.extend(conns)

        self.intersections[self.intersection_id] = intersection
        self.intersection_id += 1

        return intersection.error_turn_list

    ###########################################################################

    # 单向边复制为双向边
    def _copy_links(self, ):
        network_links = self.network_links.copy()
        for link_id, link in network_links.items():
            if not link.is_oneway:
                link1, link2 = link.shift()
                # 删
                self.network_links.pop(link_id)
                # 增
                self.network_links[link1.id] = link1
                self.network_links[link1.id] = link2

    ###########################################################################

    # 记录问题
    def _record_error(self, error_type: str, error_list: list):
        # 转向太多
        if error_type == "type1":
            error_turn_list = error_list
            for turn in error_turn_list:
                self.error_link_list["type1"].append(turn.from_link.id)
        # 交叉口的点太多
        elif error_type == "type2":
            nodes_id = error_list
            for node_id in nodes_id:
                links_id = self.network_nodes[node_id].adjacent_links
                self.error_link_list["type2"].extend(links_id)

    ###########################################################################

    # 绘制路网
    def draw(self, ):
        for link in self.network_links.values():
            x, y = link.line.xy
            plt.plot(x, y)

        for node_id, node in self.network_nodes.items():
            x, y = node.loc
            plt.text(x, y, node_id)

        plt.axis("equal")


class OsmNetwokAnalyser(BaseNetworkAnalyser):
    def analyse_all_data(self, network_data: dict, params: dict = None) -> dict:
        # 解析数据
        network = Network(**network_data)
        # network.draw()

        # 路段信息
        links_data = network.network_links
        # 连接段信息
        connectors_data = network.network_conns
        # 其他信息
        other_data = network.network_other

        standard_links_data = [
            dict(
                id=link.id,
                points=list(link.line.coords),
                lane_count=link.lane_count,
                name=f"{link.type}: {link.name}"
            )
            for link_id, link in links_data.items()
        ]
        standard_connectors_data = [
            dict(
                from_link_id=connector.from_link_id,
                to_link_id=connector.to_link_id,
                from_lane_numbers=connector.from_lane_number,
                to_lane_numbers=connector.to_lane_number,
            )
            for connector in connectors_data
        ]

        # 更新投影
        self.proj_string = other_data["proj_string"]

        return {
            "links": standard_links_data,
            "connectors": standard_connectors_data,
        }
