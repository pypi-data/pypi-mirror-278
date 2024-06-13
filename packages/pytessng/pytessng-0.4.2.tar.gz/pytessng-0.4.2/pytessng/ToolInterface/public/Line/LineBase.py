import math
from shapely.geometry import Polygon


class LineBase:
    # 计算两点间距
    @staticmethod
    def calculate_two_points_distance(p1: list, p2: list) -> float:
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

    # 求两点连线与y正轴的夹角（角度值）
    @staticmethod
    def calculate_angle_with_y_axis(p1: list, p2: list) -> float:
        x1, y1 = p1[0], p1[1]
        x2, y2 = p2[0], p2[1]
        delta_x = x2 - x1
        delta_y = y2 - y1
        # 使用 atan2 计算角度（弧度）
        angle_rad = math.atan2(delta_x, delta_y)
        # 将弧度转换为角度
        angle_deg = math.degrees(angle_rad)
        # 将角度限制在0到360
        angle_deg_with_y_axis = (angle_deg + 360) % 360
        return angle_deg_with_y_axis

    # 计算线段长度
    @staticmethod
    def calculate_line_length(line: list) -> float:
        return sum([
            LineBase.calculate_two_points_distance(line[i - 1], line[i])
            for i in range(1, len(line))
        ])

    @staticmethod
    # 根据首尾段角度计算转向类型
    def calculate_turn_type(line: list) -> str:
        start_angle = LineBase.calculate_angle_with_y_axis(line[0], line[1])
        end_angle = LineBase.calculate_angle_with_y_axis(line[-2], line[-1])
        # 角度差 -180~180
        angle_diff = (end_angle - start_angle + 180) % 360 - 180

        if -45 < angle_diff < 45:
            turn_type = "直行"
        elif -135 < angle_diff < -45:
            turn_type = "左转"
        elif 45 < angle_diff < 135:
            turn_type = "右转"
        else:
            turn_type = "掉头"

        return turn_type

    # 合并两条线段
    @staticmethod
    def merge_two_lines(line1: list, line2: list) -> list:
        new_line = []
        for p1, p2 in zip(line1, line2):
            x = (p1[0] + p2[0]) / 2
            y = (p1[1] + p2[1]) / 2
            if len(p1) == 3:
                z = p1[2] + (p2[2] - p1[2]) / 2
                p = [x, y, z]
            else:
                p = [x, y]
            new_line.append(p)
        return new_line

    # 对两点的线段进行线性插值
    @staticmethod
    def interpolate_point_on_segment(p1: list, p2: list, t: float) -> list:
        x = p1[0] + (p2[0] - p1[0]) * t
        y = p1[1] + (p2[1] - p1[1]) * t
        if len(p1) == 2:
            return [x, y]
        else:
            z = p1[2] + (p2[2] - p1[2]) * t
        return [x, y, z]

    # 获取多边形边界点
    @staticmethod
    def calculate_boundary_points(area_boundary_points: list) -> list:
        union_boundary_coords = None
        try:
            # 构建多边形对象列表
            polygon_list = [Polygon(coords) for coords in area_boundary_points]
            # 计算多边形的并集
            union_polygon = polygon_list[0]
            for polygon in polygon_list[1:]:
                union_polygon = union_polygon.union(polygon)
            # 提取边界点
            union_boundary_coords = list(union_polygon.exterior.coords)
        except:
            pass
        return union_boundary_coords
