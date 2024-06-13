from .opendrive2tessng.Opendrive2Tessng import Opendrive2Tessng
from .shape2tessng.Shape2Tessng import Shape2Tessng
from .osm2tessng.Osm2Tessng import Osm2Tessng
from .excel2tessng.Excel2Tessng import Excel2Tessng
from .json2tessng.Json2Tessng import Json2Tessng
from .zhecheng2tessng.Zhecheng2Tessng import Zhecheng2Tessng
from .aidaroe2tessng.Aidaroe2Tessng import Aidaroe2Tessng


class Other2TessngFactory:
    mode_mapping = {
        "opendrive": Opendrive2Tessng,  # file_path: str, step_length: float, lane_types: list
        "shape": Shape2Tessng,  # folder_path: str, is_use_lon_and_lat: bool, is_use_center_line: bool, lane_file_name: str, lane_connector_file_name: str, proj_mode: str
        "osm": Osm2Tessng,  # file_path: str, bounding_box: dict, center_point: dict, road_class: int, proj_mode: str, save_data_path: str
        "excel": Excel2Tessng,  # file_path: str
        "json": Json2Tessng,  # file_path: str
        "zhecheng": Zhecheng2Tessng,  # folder_path: str, file_path: str
        "aidaroe": Aidaroe2Tessng,  # file_path: str
    }

    @classmethod
    def build(cls, netiface, mode: str, params: dict) -> dict:
        if mode in cls.mode_mapping:
            model = cls.mode_mapping[mode](netiface)
            response = model.load_data(params)
            return response
        else:
            raise Exception("No This Import Mode!")
