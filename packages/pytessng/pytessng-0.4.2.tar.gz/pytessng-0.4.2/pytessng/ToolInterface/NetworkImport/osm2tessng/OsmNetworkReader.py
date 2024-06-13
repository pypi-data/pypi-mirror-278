import os
import json
import math
import random
import traceback
from datetime import datetime
import xml.etree.ElementTree as ET
from pyproj import Proj
import osmnx as ox

from pytessng.Config import NetworkImportConfig
from pytessng.Logger import logger
from pytessng.ProgressDialog import ProgressDialogClass as pgd


class OSMNetworkReader:
    """
    1.params：
        (1) file_path (optional) str
            e.g.
                file_path = "nanjing.osm"
        (2) bounding_box (optional) dict
            e.g.
                bounding_box = {
                    "lon_min": 113.80543,
                    "lon_max": 114.34284,
                    "lat_min": 29.69543,
                    "lat_max": 31.84852,
                }
        (3) center_point (optional) dict
            e.g.
                center_point = {
                    "lon_0": 113.80543,
                    "lat_0": 31.84852,
                    "distance": 5, # (km)
                }
        (4) road_class (optional) int [1, 2, 3]
            1: 高速公路
            2: 高速公路和城市主干路
            3: 高速公路、城市主干路和低等级道路 (default)
        (5) proj_mode (optional) str [tmerc, utm, web]
            tmerc: 高斯克吕格投影
            utm: 通用横轴墨卡托投影
            web: Web墨卡托投影 (default)
        (6) save_data_path

    2.可以通过get_osm_data()来获取路网信息，包括：
        (1) edges_info;
        (2) nodes_info;
        (3) other_info.
    """

    road_class_type = NetworkImportConfig.OSM.ROAD_CLASS_TYPE
    default_road_class = NetworkImportConfig.OSM.DEFAULT_ROAD_CLASS
    default_lane_count = NetworkImportConfig.OSM.DEFAULT_LANE_COUNT
    default_lane_width = NetworkImportConfig.OSM.DEFAULT_LANE_WIDTH

    def __init__(self, params: dict):
        self.params = params

        self.edges_info = None
        self.nodes_info = None
        self.other_info = {
            "data_source": "OpenStreetMap",
            "created_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "proj_string": "EPSG:3857",
            "move_distance": {"x_move": 0, "y_move": 0},
            "scene_center": {"lon_0": None, "lat_0": None},
            "scene_bounding": {"lon_min": None, "lon_max": None, "lat_min": None, "lat_max": None},
            "scene_size": {"width": None, "height": None},
        }

        # 道路类型
        self.road_type = self._get_road_type()  # dict
        # 投影
        self.p = None
        # 图对象
        self.G = None

        # 设置缓存路径和取消API限速
        self.save_data_path = self.params.get("save_data_path") or os.path.join(os.getcwd(), "osm_data")
        self.save_before_process_data_path = os.path.join(self.save_data_path, "before_process")
        self.save_after_process_data_path = os.path.join(self.save_data_path, "after_process")
        ox.settings.cache_folder = self.save_before_process_data_path
        ox.settings.overpass_rate_limit = False
        # 创建保存文件夹
        os.makedirs(self.save_before_process_data_path, exist_ok=True)
        os.makedirs(self.save_after_process_data_path, exist_ok=True)

        # 获取图对象
        self._get_osm_graph_object()
        # 解析图对象
        if self.G:
            self._get_osm_json_data()

    # 获取图对象
    def _get_osm_graph_object(self) -> None:
        if self.params.get("file_path"):
            self._get_osm_graph_object_by_osm_file_path()
        elif self.params.get("bounding_box"):
            self._get_osm_graph_object_by_bounding_box()
        elif self.params.get("center_point"):
            self._get_osm_graph_object_by_center_point()
        else:
            logger.logger_pytessng.error("No initialization information!")
            return

        logger.logger_pytessng.debug("Graph object obtaining is finished!")

    # 解析osm文件
    def _get_osm_graph_object_by_osm_file_path(self) -> None:
        try:
            pgd().update_progress(random.randint(10,20), 100, "数据解析中（1/7）")
            self.G = ox.graph_from_xml(self.params["file_path"])
            pgd().update_progress(100, 100, "数据解析中（1/7）")
        except:
            logger.logger_pytessng.error(f"The OSM file cannot be parsed with the error: {traceback.format_exc()}!")

        try:
            # 解析XML文件
            tree = ET.parse(self.params["file_path"])
            root = tree.getroot()
            # 获取bounds元素的属性
            bounds_element = root.find('bounds')
            lat_min = float(bounds_element.get('minlat'))
            lon_min = float(bounds_element.get('minlon'))
            lat_max = float(bounds_element.get('maxlat'))
            lon_max = float(bounds_element.get('maxlon'))
        except:
            lons, lats = [], []
            for u, v, key, data in self.G.edges(keys=True, data=True):
                for node_id in [u, v]:
                    lon = self.G.nodes[node_id]['x']
                    lat = self.G.nodes[node_id]['y']
                    lons.append(lon)
                    lats.append(lat)
            lon_min, lon_max = min(lons), max(lons)
            lat_min, lat_max = min(lats), max(lats)
        bounding_box = {
            "lon_min": lon_min,
            "lon_max": lon_max,
            "lat_min": lat_min,
            "lat_max": lat_max,
        }

        # 四边界经纬度
        self.other_info["scene_bounding"].update(bounding_box)
        # 中心经纬度
        lon_0, lat_0 = OSMNetworkReader.calculate_center_coordinates(**bounding_box)
        self.other_info["scene_center"].update({"lon_0": lon_0, "lat_0": lat_0})
        # 投影和move
        self._get_proj_string_and_move_distance()
        # 场景尺寸
        width, height = OSMNetworkReader.calculate_scene_size(lon_0, lat_0, lon_min, lon_max, lat_min, lat_max, self.p)
        self.other_info["scene_size"].update({"width": width, "height": height})

    # 指定四边界拉取数据
    def _get_osm_graph_object_by_bounding_box(self) -> None:
        bounding_box = self.params["bounding_box"]
        lon_min = bounding_box["lon_min"]
        lon_max = bounding_box["lon_max"]
        lat_min = bounding_box["lat_min"]
        lat_max = bounding_box["lat_max"]

        # 四边界经纬度
        self.other_info["scene_bounding"].update(bounding_box)
        # 中心经纬度
        lon_0, lat_0 = OSMNetworkReader.calculate_center_coordinates(**bounding_box)
        self.other_info["scene_center"].update({"lon_0": lon_0, "lat_0": lat_0})
        # 投影和move
        self._get_proj_string_and_move_distance()
        # 场景尺寸
        width, height = OSMNetworkReader.calculate_scene_size(lon_0, lat_0, lon_min, lon_max, lat_min, lat_max, self.p)
        self.other_info["scene_size"].update({"width":width, "height":height})

        try:
            pgd().update_progress(random.randint(10,20), 100, "数据解析中（1/7）")
            self.G = ox.graph_from_bbox(lat_max, lat_min, lon_max, lon_min, **self.road_type)
            pgd().update_progress(100, 100, "数据解析中（1/7）")
        except:
            logger.logger_pytessng.error(f"Due to network connectivity issues, OpenStreetMap data acquisition failed with the error: {traceback.format_exc()}!")

    # 指定中心和半径拉取数据
    def _get_osm_graph_object_by_center_point(self) -> None:
        lon_0 = self.params["center_point"]["lon_0"]
        lat_0 = self.params["center_point"]["lat_0"]
        distance = self.params["center_point"]["distance"] * 1000 # m

        # 中心经纬度
        self.other_info["scene_center"].update({"lon_0": lon_0, "lat_0": lat_0})
        # 投影和move
        self._get_proj_string_and_move_distance()
        # 场景尺寸
        self.other_info["scene_size"].update({"width": round(distance*2,1), "height": round(distance*2,1)})
        # 四边界经纬度
        lon_min, lon_max, lat_min, lat_max = OSMNetworkReader.calculate_bounding_coordinates(distance, self.p)
        self.other_info["scene_bounding"].update({"lon_min":lon_min,"lon_max":lon_max,"lat_min":lat_min,"lat_max":lat_max})

        try:
            pgd().update_progress(random.randint(10,20), 100, "数据解析中（1/7）")
            self.G = ox.graph_from_point((lat_0, lon_0), distance, **self.road_type)
            pgd().update_progress(100, 100, "数据解析中（1/7）")
        except:
            logger.logger_pytessng.error(f"Due to network connectivity issues, OpenStreetMap data acquisition failed with the error: {traceback.format_exc()}!")

    # 获取应该拉取的路段类型
    def _get_road_type(self):
        road_class = self.params.get("road_class", self.default_road_class)
        # 只有高速公路
        if road_class == 1:
            road_type = {"custom_filter": '["highway"~"motorway|motorway_link"]'}
        # 有高速公路和主干路
        elif road_class == 2:
            road_type = {"custom_filter": '["highway"~"motorway|motorway_link|trunk|primary|secondary|tertiary"]'}
        # 所有道路都有
        else:
            road_type = {"network_type": "drive"}
        return road_type

    # 获取投影和move
    def _get_proj_string_and_move_distance(self):
        lon_0 = self.other_info["scene_center"]["lon_0"]
        lat_0 = self.other_info["scene_center"]["lat_0"]
        # 投影
        proj_mode = self.params.get("proj_mode")
        if proj_mode == "tmerc":
            self.other_info["proj_string"] = f'+proj=tmerc +lon_0={lon_0} +lat_0={lat_0} +ellps=WGS84'
        elif proj_mode == "utm":
            self.other_info["proj_string"] = f'+proj=utm +zone={lon_0//6+31} +ellps=WGS84'
        self.p = Proj(self.other_info["proj_string"])
        # move
        x_move, y_move = OSMNetworkReader.calculate_move_distance(lon_0, lat_0, self.other_info["proj_string"])
        self.other_info["move_distance"].update({"x_move": x_move, "y_move": y_move})

    # 解析图对象
    def _get_osm_json_data(self) -> None:
        edges_info = {}
        nodes_info = {}

        edge_id_list = []
        node_id_dict = {}
        edge_num = 0
        node_num = 0

        road_class = self.params.get("road_class", self.default_road_class)
        # u：起始节点编号，v：目标节点编号，key：同一对节点的不同边的编号
        for u, v, key, data in pgd.progress(self.G.edges(keys=True, data=True), '数据解析中（2/7）'):
            for node_id in [u, v]:
                if node_id not in node_id_dict:
                    node_num += 1
                    node_id_dict[node_id] = node_num

            edge_id = f"{min(u, v)}-{max(u, v)}"
            if edge_id in edge_id_list:
                continue
            else:
                edge_id_list.append(edge_id)

            # 道路类型
            highway = data.get("highway")
            if type(highway) == list:
                highway = highway[0]
            if self.road_class_type.get(road_class) and highway not in self.road_class_type[road_class]:
                continue

            # 车道数(int or list or None)
            laneCount = data.get("lanes")

            # 道路类型不同，默认车道数不同
            try:
                if laneCount is None:
                    laneCount = self.default_lane_count.get(str(highway)) or self.default_lane_count["other"]
                elif type(laneCount) == list:
                    laneCount = max(list(map(int, laneCount)))
                else:
                    laneCount = int(laneCount)
            except:
                logger.logger_pytessng.error(f"Lane Count with the error: {traceback.format_exc()}")
                # 有错误就为1
                laneCount = 1

            # 点位信息
            try:
                # 有点位信息就用点位信息
                geometry = [self.p(x, y) for x, y in list(data.get('geometry').coords)]
            except:
                # 没有点位信息就用起终点的坐标
                point_start = self.p(self.G.nodes[u]['x'], self.G.nodes[u]['y'])
                point_end = self.p(self.G.nodes[v]['x'], self.G.nodes[v]['y'])
                geometry = [point_start, point_end]

            # 是单向道路(True)还是双向道路(False)
            oneway = data["oneway"]

            # 路段名称
            name = data.get("name", "")
            if type(name) == list:
                name = ",".join(name)

            edge_num += 1
            edges_info[edge_num] = {
                "start_node_id": node_id_dict[u],
                "end_node_id": node_id_dict[v],
                "geometry": geometry,
                "lane_count": laneCount,
                "highway": highway,
                "is_oneway": oneway,
                "name": name,
            }

            if highway not in self.road_class_type[2]:
                continue

            for old_node_id in [u, v]:
                new_node_id = node_id_dict[old_node_id]
                if new_node_id not in nodes_info:
                    loc = self.p(self.G.nodes[old_node_id]['x'], self.G.nodes[old_node_id]['y'])
                    nodes_info[new_node_id] = {"loc": loc, "adjacent_links": []}
                nodes_info[new_node_id]["adjacent_links"].append(edge_num)

        self.edges_info = edges_info
        self.nodes_info = nodes_info

    # 给定四边界，计算中心经纬度
    @staticmethod
    def calculate_center_coordinates(lon_min: float, lon_max: float, lat_min: float, lat_max: float) -> (float, float):
        # 计算中心经度
        lon_center = (lon_min + lon_max) / 2
        # 将角度转换为弧度
        lat_min_rad = math.radians(lat_min)
        lat_max_rad = math.radians(lat_max)
        # 计算中心纬度
        dx = math.sin(lat_min_rad) + math.sin(lat_max_rad)
        dy = math.cos(lat_min_rad) + math.cos(lat_max_rad)
        lat_center = math.degrees(math.atan2(dx, dy))
        return lon_center, lat_center

    # 给定中心和长度m，计算边界经纬度
    @staticmethod
    def calculate_bounding_coordinates(distance: float, proj) -> (float, float, float, float):
        lon_max, _ = proj(distance, 0, inverse=True)
        lon_min, _ = proj(-distance, 0, inverse=True)
        _, lat_max = proj(0, distance, inverse=True)
        _, lat_min = proj(0, -distance, inverse=True)
        return lon_min, lon_max, lat_min, lat_max

    # 给定中心经纬度和四边界经纬度，计算场景尺寸
    @staticmethod
    def calculate_scene_size(lon_0: float, lat_0: float, lon_min: float, lon_max: float, lat_min: float, lat_max: float, proj) -> (float, float):
        east, _ = proj(lon_max, lat_0)
        west, _ = proj(lon_min, lat_0)
        _, north = proj(lon_0, lat_max)
        _, south = proj(lon_0, lat_min)
        width = round(east - west, 1)
        height = round(north - south, 1)
        return width, height

    # 确定移动场景到中心的距离
    @staticmethod
    def calculate_move_distance(lon_0: float, lat_0: float, proj_string: str) -> (float, float):
        p = Proj(proj_string)
        x_0, y_0 = p(lon_0, lat_0)
        x_move, y_move = -x_0, -y_0
        return x_move, y_move

    # 从外部获取数据
    def get_osm_data(self, save_file_name: str = "") -> dict:
        osm_data = {
            "edges_info": self.edges_info,
            "nodes_info": self.nodes_info,
            "other_info": self.other_info,
        }
        # 默认保存名称
        if not save_file_name:
            save_file_name = self.other_info["created_time"].replace('-', '').replace(':', '').replace(' ', '')
        if self.G:
            save_path = os.path.join(self.save_after_process_data_path, f'{save_file_name}.json')
            with open(save_path, 'w', encoding="utf-8") as json_file:
                json.dump(osm_data, json_file, indent=4, ensure_ascii=False)
            logger.logger_pytessng.info("Data saving is finished!")
        else:
            logger.logger_pytessng.error("The graph object has not been initialized!")
        return osm_data
