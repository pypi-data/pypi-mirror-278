import math


# 计算给定经度下两个纬度点的中心位置的纬度和经度
class CenterPointCalculator:
    @staticmethod
    def calculate_center_point(lon_min: float, lon_max: float, lat_min: float, lat_max: float) -> (float, float):
        # 计算中心位置的经度
        lon_center = (lon_min + lon_max) / 2

        # 将纬度和经度从度数转换为弧度
        lat1 = math.radians(lat_min)
        lat2 = math.radians(lat_max)
        # 计算中心位置的纬度
        lat_center = (lat1 + lat2) / 2
        # 将中心位置的纬度和经度从弧度转换为度数
        lat_center = math.degrees(lat_center)

        return lon_center, lat_center
