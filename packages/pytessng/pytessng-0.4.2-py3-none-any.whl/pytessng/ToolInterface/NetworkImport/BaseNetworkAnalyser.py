from abc import ABC, abstractmethod


class BaseNetworkAnalyser(ABC):
    def __init__(self):
        # 投影
        self.proj_string = ""

    @abstractmethod
    def analyse_all_data(self, network_data, params: dict = None) -> dict:
        pass
