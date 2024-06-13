from pytessng.ProgressDialog import ProgressDialogClass as pgd


class LinkGroupsSearcher:
    def __init__(self, netiface, existing_links_data: dict, existing_connectorAreas_data: dict):
        self.netiface = netiface
        self.existing_links_data = existing_links_data
        self.existing_connectorAreas_data = existing_connectorAreas_data

    def get_link_groups(self) -> dict:
        link_groups = []
        # 已经查找过的路段ID
        exist_links = []

        for link_id, link_data in pgd.progress(self.existing_links_data.items(), "可合并路段搜索中（1/6）"):
            # 已经查找过了
            if link_id in exist_links:
                continue

            link_group = [link_id]
            self.get_chain_by_next(link_id, link_group)
            self.get_chain_by_last(link_id, link_group)

            if len(link_group) >= 2:
                link_groups.append(link_group)
            exist_links.extend(link_group)

        # 判断是否有路段进行过重复查询，如果有，说明逻辑存在漏洞
        if len(exist_links) != len(set(exist_links)):
            print("出现唯一性错误，请联系开发者")
            return dict()

        return {
            index: link_groups
            for index, link_groups in enumerate(link_groups, start=10000)
        }

    # 向下游搜索
    def get_chain_by_next(self, link_id: int, link_group: list) -> None:
        # 本路段只有一个下游路段
        next_link_ids = self.existing_links_data[link_id]["next_link_ids"]
        if len(next_link_ids) == 1:
            next_link_id = next_link_ids[0]
            # 下游路段没有搜索过：如果有说明形成了回路
            if next_link_id not in link_group:
                is_connectible = self.get_is_connectible(link_id, next_link_id)
                # 如果可合并
                if is_connectible:
                    link_group.append(next_link_id)
                    self.get_chain_by_next(next_link_id, link_group)

    # 向上游搜索
    def get_chain_by_last(self, link_id: int, link_group: list) -> None:
        # 本路段只有一个上游路段
        last_link_ids = self.existing_links_data[link_id]["last_link_ids"]
        if len(last_link_ids) == 1:
            last_link_id = last_link_ids[0]
            # 上游路段没有搜索过：如果有说明形成了回路
            if last_link_id not in link_group:
                is_connectible = self.get_is_connectible(last_link_id, link_id)
                # 如果可合并
                if is_connectible:
                    link_group.insert(0, last_link_id)
                    self.get_chain_by_last(last_link_id, link_group)

    # 判断是否可连接
    def get_is_connectible(self, fist_link_id: int, second_link_id: int) -> bool:
        fist_link_next_link_ids = self.existing_links_data[fist_link_id]["next_link_ids"]
        second_link_last_link_ids = self.existing_links_data[second_link_id]["last_link_ids"]

        # 上游路段只有一个下游路段
        if len(fist_link_next_link_ids) != 1:
            return False

        # 下游路段只有一个上游路段
        if len(second_link_last_link_ids) != 1:
            return False

        first_link = self.netiface.findLink(fist_link_id)
        second_link = self.netiface.findLink(second_link_id)
        first_link_lane_actions = [lane.actionType() for lane in first_link.lanes()]
        second_link_lane_actions = [lane.actionType() for lane in second_link.lanes()]

        # 各车道类型相同
        if first_link_lane_actions != second_link_lane_actions:
            return False

        connector = self.netiface.findConnectorByLinkIds(fist_link_id, second_link_id)

        # 车道连接的数量不能缺失
        if len(connector.laneConnectors()) != len(first_link.lanes()):
            return False

        # 即使路段只有一个上游，连接段所属面域中存在多个连接段，仍然不允许合并
        for value in self.existing_connectorAreas_data.values():
            if connector.id() in value and len(value) >= 3:
                if "非机动车道" in first_link_lane_actions:
                    print(f"Warning: 面域内连接段过多, 进入交叉口区域, 不再继续: {value}")
                    return False
                else:
                    print(f"Ignorewarning: 面域内连接段过多, 但是还要继续: {value}")

        return True
