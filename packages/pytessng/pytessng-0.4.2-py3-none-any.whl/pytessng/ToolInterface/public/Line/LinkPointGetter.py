from .LineBase import LineBase
from pytessng.Logger import logger


class LinkPointGetter:
    """ 根据距离计算线上的点的位置 """
    @staticmethod
    def get_point_by_dist(road_centerline: list, target_distance: float) -> list:
        target_location = []

        if target_distance < 0:
            logger.logger_pytessng.warning(f"LinkPointGetter waring 1: [target_distance: {target_distance}]")
            return target_location

        current_distance = 0.0
        for i in range(len(road_centerline) - 1):
            current_point = road_centerline[i]
            next_point = road_centerline[i + 1]
            segment_distance = LineBase.calculate_two_points_distance(current_point, next_point)

            if current_distance + segment_distance >= target_distance:
                remaining_distance = target_distance - current_distance
                target_location = LineBase.interpolate_point_on_segment(current_point, next_point, remaining_distance)
                break

            current_distance += segment_distance

        # 超出范围
        if target_location == []:
            logger.logger_pytessng.warning(f"LinkPointGetter waring 2: [current_distance: {current_distance:.3f}] [target_distance: {target_distance:.3f}]")
            if abs(target_distance - current_distance) <= 2:
                target_location = road_centerline[-1]

        return target_location
