from abc import abstractmethod

from ..BaseTool import BaseTool


class BaseTessng2Other(BaseTool):
    def load_data(self, params: dict):
        # 获取参数
        file_path = params["file_path"]
        proj_string = params["proj_string"]

        # 解析数据
        network_data = self.analyze_data(self.netiface, proj_string)
        # 保存数据
        self.save_data(network_data, file_path)

    @abstractmethod
    def analyze_data(self, netiface, proj_string: str = None):
        pass

    @abstractmethod
    def save_data(self, network_data, file_path: str):
        pass
