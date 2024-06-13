from collections import defaultdict

from ..BaseTool import BaseTool


class NetworkIterator(BaseTool):
    # 获取已有路段数据
    def get_existing_links_data(self) -> dict:
        links_data = {}

        # 遍历路段
        for link in self.netiface.links():
            link_id = link.id()
            links_data[link_id] = {
                "link_id": link_id,
                "last_link_ids": [],
                "next_link_ids": [],
            }

        # 遍历连接段
        for connector in self.netiface.connectors():
            last_link = connector.fromLink()
            next_link = connector.toLink()

            links_data[last_link.id()]["next_link_ids"].append(next_link.id())
            links_data[next_link.id()]["last_link_ids"].append(last_link.id())

        return links_data

    # 获取已有连接段面域数据
    def get_connectorAreas_data(self) -> dict:
        connector_areas_data = defaultdict(list)

        # 遍历连接段面域
        for ConnectorArea in self.netiface.allConnectorArea():
            for connector in ConnectorArea.allConnector():
                connector_areas_data[ConnectorArea.id()].append(connector.id())

        return connector_areas_data
