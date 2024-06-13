import os
import logging
from pyautogui import size as scene_size


class LoggingConfig:
    # 记录到文件
    FILE_LOGS_LEVEL = logging.DEBUG
    # 打印在控制台
    CONSOLE_LOGS_LEVEL = logging.DEBUG


class PathConfig:
    # 文件所在文件夹的路径
    THIS_FILE_PATH = os.path.dirname(__file__)
    # 进程(工作空间)的路径
    WORKSPACE_PATH = os.path.join(os.getcwd(), "WorkSpace")

    # (1) UUID的路径
    UUID_FILE_PATH = os.path.join(os.environ['USERPROFILE'], ".pytessng")
    # (2) ico图标的路径
    ICON_FILE_PATH = os.path.join(THIS_FILE_PATH, "Files", "Ico", "TESSNG.ico")
    # (3) 说明书的路径
    INSTRUCTION_FILE_PATH = os.path.join(THIS_FILE_PATH, "Files", "Doc", "用户使用手册.pdf")
    # (4) 样例文件的路径
    EXAMPLES_DIR_PATH = "file:\\" + os.path.join(WORKSPACE_PATH, "Examples")
    # (5) 日志文件的路径
    LOG_DIR_PATH = os.path.join(WORKSPACE_PATH, "Log")
    # (6) 默认创建路网打开文件和导出路网保存数据的路径（会有更改）
    OPEN_DIR_PATH = os.path.join(WORKSPACE_PATH, "Examples")  # 是在样例文件夹
    # (7) 导出轨迹保存为Json的路径
    DEFAULT_SAVE_TRAJ_DIR_PATH = os.path.join(WORKSPACE_PATH, "Data", "traj_data")
    # (8) osm数据保存的路径
    DEFAULT_SAVE_OSM_DIR_PATH = os.path.join(WORKSPACE_PATH, "Data", "osm_data")


class NetworkImportConfig:
    # 车道类型映射 for OpenDrive/Shape
    LANE_TYPE_MAPPING = {
        'driving': '机动车道',
        'biking': '非机动车道',
        'sidewalk': '非机动车道',
        'stop': '应急车道',
        # OpenDrive
        'onRamp': '机动车道',
        'offRamp': '机动车道',
        'entry': '机动车道',
        'exit': '机动车道',
        'connectingRamp': '机动车道',
        'shoulder': '应急车道',
        'parking': '停车带',
    }

    class OpenDrive:
        # 如果是opendrive导入的路网，会主动进行简化(仅路段)，避免创建过慢
        simplify_network_force = True

        # 当前后几个点的向量夹角小于 default_angle 且点距小于 max_length(除非夹角为0) 时，抹除过渡点
        default_angle = 1
        max_length = 50

        # 连续次数后可视为正常车道，或者连续次数后可视为连接段,最小值为2
        POINT_REQUIRE = 2

        # 当 opendrive 连接段的首尾连接长度低于此值时，抛弃原有的点序列，使用自动连接
        MIN_CONNECTOR_LENGTH = None

        # 需要被处理的车道类型及处理参数
        WIDTH_LIMIT = {
            '机动车道': {
                'split': 2,  # 作为正常的最窄距离
                'join': 1.5,  # 被忽略时的最宽距离
            },
            '非机动车道': {
                'split': 2,
                'join': 0.5,
            },
        }

        # 拓宽连接段时的路段裁剪长度
        SPLIT_LENGTH = 2

    class Shape:
        # 车道默认宽度
        DEFAULT_LANE_WIDTH_MAPPING = {
            "driving": 3.5,
            "biking": 1.5,
            "sidewalk": 1.5,
            "stop": 3.5
        }
        # 小于该宽度的车道要删除
        MIN_LANE_WIDTH = 2.5  # m

        # 检查最长的车道与最短的车道的长度差是否在一定范围内
        MAX_LENGTH_DIFF = 20  # m
        # 各条车道的起终点距离上下限
        MAX_DISTANCE_LANE_POINTS = 9  # m
        MIN_DISTANCE_LANE_POINTS = 0  # m
        # 寻点距离
        MAX_DISTANCE_SEARCH_POINTS = 2.8  # m

    class OSM:
        # 拉取的路段类型
        ROAD_CLASS_TYPE = {
            1: ["motorway", "motorway_link"],
            2: [
                "motorway", "motorway_link",
                "trunk", "trunk_link",
                "primary", "primary_link",
                "secondary", "secondary_link",
                "tertiary", "tertiary_link"
            ],
        }

        # 不同道路类型的默认车道数
        DEFAULT_LANE_COUNT = {
            "motorway": 3,
            "motorway_link": 2,
            "trunk": 3,
            "trunk_link": 2,
            "primary": 3,
            "primary_link": 1,
            "secondary": 2,
            "secondary_link": 1,
            "tertiary": 2,
            "tertiary_link": 1,
            "other": 1,
        }
        # 默认路段类型等级
        DEFAULT_ROAD_CLASS = 3

        # 车道宽度
        DEFAULT_LANE_WIDTH = 3.5

    class Aidaroe:
        # 去除超窄车道的阈值（m）
        THRESHOLD_LANE_WIDTH = 0.5

        # 去除超短路段的阈值（m）
        THRESHOLD_LINK_LENGTH = 2

        # 车辆类型映射
        VEHI_TYPE_CODE_MAPPING = {100: 1, 200: 2, 300: 4}

        # 车辆输入、决策路径、信号灯组的生效时长（s）
        VALID_DURATION = 12 * 3600


class NetworkExportConfig:
    # 车道类型映射 for OpenDrive/Shape
    LANE_TYPE_MAPPING = {
        '机动车道': 'driving',
        '非机动车道': 'biking',
        '人行道': 'sidewalk',
        '应急车道': 'stop',
    }

    class Unity:
        # 属性映射关系
        CONVERT_ATTRIBUTE = {
            "black": "Driving",
            "white": "WhiteLine",
            "yellow": "YellowLine",
        }

        # 线宽
        BORDER_LINE_WIDTH = 0.2  # m
        CENTER_LINE_WIDTH = 0.3  # m

        # # 虚实线长度
        # empty_line_length = 3  # m
        # real_line_length = 4  # m


class LinkEditConfig:
    DEFAULT_MAX_LINK_LENGTH = 1000  # m
    DEFAULT_MIN_CONNECTOR_LENGTH = 10  # m
    # UI
    MIN_MAX_LINK_LENGTH = 50  # m
    MAX_MAX_LINK_LENGTH = 5000  # m
    MIN_MIN_CONNECTOR_LENGTH = 0.1  # m
    MAX_MIN_CONNECTOR_LENGTH = 100  # m

    class Creator:
        # UI
        DEFAULT_LANE_WIDTH = 3.5
        MIN_LANE_WIDTH = 0.5
        MAX_LANE_WIDTH = 10

    class Locator:
        DIST = 4  # m

    class Merger:
        DEFAULT_INCLUDE_CONNECTOR = True
        DEFAULT_SIMPLIFY_POINTS = True

    class SIMPLIFIER:
        DEFAULT_MAX_DISTANCE = 0.3  # m
        DEFAULT_MAX_LENGTH = 1000  # m
        # UI
        MIN_MAX_DISTANCE = 0.05  # m
        MAX_MAX_DISTANCE = 10  # m
        MIN_MAX_LENGTH = 50  # m
        MAX_MAX_LENGTH = 5000  # m


class SimuExportConfig:
    class Kafka:
        TEST_TOPIC = "pytessng_test"


class UIConfig:
    class Menu:
        extension_list = [
            ("network_import", ["json"]),
            ("network_export", ["unity", "json"]),
            ("link_edit", ["create", "split"]),
            ("file_export", "all")
        ]

    class Base:
        width: int = int(scene_size()[0] / 4)
        height: int = 200

    class BaseLinkEdit:
        width: int = 250
        height: int = 150

    class FileExportPilenumber:
        width: int = int(scene_size()[0] / 2)
