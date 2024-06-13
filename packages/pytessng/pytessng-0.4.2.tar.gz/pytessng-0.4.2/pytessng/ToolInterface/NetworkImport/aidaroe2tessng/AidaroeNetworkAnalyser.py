from ..BaseNetworkAnalyser import BaseNetworkAnalyser
from pytessng.Config import NetworkImportConfig
from pytessng.ProgressDialog import ProgressDialogClass as pgd


class AidaroeNetworkAnalyser(BaseNetworkAnalyser):
    threshold_lane_width = NetworkImportConfig.Aidaroe.THRESHOLD_LANE_WIDTH
    threshold_link_length = NetworkImportConfig.Aidaroe.THRESHOLD_LINK_LENGTH
    vehiTypeCode_mapping = NetworkImportConfig.Aidaroe.VEHI_TYPE_CODE_MAPPING
    valid_duration = NetworkImportConfig.Aidaroe.VALID_DURATION

    def analyse_all_data(self, data, params: dict = None) -> dict:
        # 路网名称
        # network_name = data.get("ioname", "")
        # 解析路段和连接段
        links_data, connectors_data = self.analyse_links_and_connectors(data["links"], data["connectors"])
        # 解析车辆组成
        vehicleCompositions_data = self.analyse_vehicleCompositions(data["vehicleCompositions"])
        # 解析车辆输入
        vehicleInputs_data = self.analyse_vehicleInputs(data["vehicleInputs"])
        # 解析信号灯组及相位
        signalGroups_data = self.analyse_signalGroups(data["sigs"])
        # 解析信号灯头
        signalHeads_data = self.analyse_signalHeads(data["signalHeads"])
        # 解析决策点
        decisionPoints_data = self.analyse_decisionPoints(data["vehicleRoutingDecisionsStatic"])
        # 解析减速区
        reducedSpeedAreas_data = self.analyse_reducedSpeedAreas(data["reducedSpeedAreas"])
        return {
            # "network_name": network_name,
            "links": links_data,
            "connectors": connectors_data,
            "vehicleCompositions": vehicleCompositions_data,
            "vehicleInputs": vehicleInputs_data,
            "signalGroups": signalGroups_data,
            "signalHeads": signalHeads_data,
            "decisionPoints": decisionPoints_data,
            "reducedSpeedAreas": reducedSpeedAreas_data,
        }

    # 解析路段和连接段
    def analyse_links_and_connectors(self, original_links_data: dict, original_connectors_data: dict) -> (list, list):
        # 解析路段
        def _analyse_links(original_links_data_: dict) -> dict:
            links_data = {}
            for link in pgd.progress(original_links_data_, "路段数据解析中(1/12)"):
                link_id = str(link["no"])
                link_name = link["name"] or link_id
                link_points = link["point3Ds"]
                link_length = link["len"]
                lanes_width = link["laneWidths"]
                links_data[link_id] = {
                    "link_name": link_name,
                    "link_points": link_points,
                    "link_length": link_length,
                    "lanes_width": lanes_width,
                    "from_link_and_conn": [],
                    "to_link_and_conn": [],
                }
            return links_data

        # 解析连接段
        def _analyse_connectors(original_connectors_data_: dict, links_data_: dict) -> dict:
            connectors_data = {}
            for connector in pgd.progress(original_connectors_data_, "连接段数据解析中(2/12)"):
                from_link_id = str(connector["fromLinkEndPt"][0])
                to_link_id = str(connector["toLinkEndPt"][0])

                # 构建连接段ID
                connector_id = f"{from_link_id}-{to_link_id}"
                if connector_id not in connectors_data:
                    connectors_data[connector_id] = {
                        "from_lane_numbers": [],
                        "to_lane_numbers": []
                    }

                # 更新路段数据
                links_data_[from_link_id]["to_link_and_conn"].append([to_link_id, connector_id])
                links_data_[to_link_id]["from_link_and_conn"].append([from_link_id, connector_id])

                # 计算车道序号
                lane_num = connector["laneNum"]
                from_lane_numbers = [connector["fromLinkEndPt"][1] + num for num in range(lane_num)]  # start from one
                to_lane_numbers = [connector["toLinkEndPt"][1] + num for num in range(lane_num)]  # start from one

                # 保存连接段数据
                connectors_data[connector_id]["from_lane_numbers"].extend(from_lane_numbers)
                connectors_data[connector_id]["to_lane_numbers"].extend(to_lane_numbers)
                # 排序
                connectors_data[connector_id]["from_lane_numbers"].sort()
                connectors_data[connector_id]["to_lane_numbers"].sort()

            return connectors_data

        # 去掉超窄车道，并更新路段和连接段数据
        def _handle_narrow_lanes(links_data_: dict, connectors_data_: dict) -> None:
            for link_id, link in pgd.progress(links_data_.items(), "超窄车道处理中(3/12)"):
                # 判断是否有超窄车道
                lanes_width = link["lanes_width"]
                new_lanes_width = [width for width in lanes_width if width >= self.threshold_lane_width]

                # 如果有超窄车道
                if len(new_lanes_width) != len(lanes_width):
                    # 车道序号映射
                    lane_no_mapping = {}
                    for index, lane_width in enumerate(lanes_width, start=1):
                        if lane_width > 0.5:
                            lane_no_mapping[index] = index
                        else:
                            # 假定超窄车道在最左侧或最右侧
                            if index == 1:
                                lane_no_mapping[index] = index + 1
                            elif index == len(lanes_width):
                                lane_no_mapping[index] = index - 1
                            else:
                                raise ValueError("Unexpected narrow lane found.")
                    # 车道序号需要减去的值
                    shift = min(lane_no_mapping.values()) - 1

                    # 更新路段数据
                    link["lanes_width"] = new_lanes_width
                    # 更新下游连接段数据
                    for to_link_id, to_conn_id in link["to_link_and_conn"]:
                        lane_numbers = connectors_data_[to_conn_id]["from_lane_numbers"]
                        connectors_data_[to_conn_id]["from_lane_numbers"] = [
                            lane_no_mapping[lane_number] - shift
                            for lane_number in lane_numbers
                        ]
                    # 更新上游连接段数据
                    for from_link_id, from_conn_id in link["from_link_and_conn"]:
                        lane_numbers = connectors_data_[from_conn_id]["to_lane_numbers"]
                        connectors_data_[from_conn_id]["to_lane_numbers"] = [
                            lane_no_mapping[lane_number] - shift
                            for lane_number in lane_numbers
                        ]

        # 去除超短路段，并更新路段和连接段数据
        def _handle_short_links(links_data_: dict, connectors_data_: dict) -> None:
            for link_id, link in pgd.progress(links_data_.copy().items(), "超短路段处理中(4/12)"):
                link_length = link["link_length"]

                if link_length < self.threshold_link_length:
                    from_link_and_conn = link["from_link_and_conn"]  # list
                    to_link_and_conn = link["to_link_and_conn"]  # list
                    if not from_link_and_conn or not to_link_and_conn:
                        continue

                    # 两层遍历
                    for from_link_id, from_conn_id in from_link_and_conn:
                        for to_link_id, to_conn_id in to_link_and_conn:
                            # 构建新的连接段ID
                            new_conn_id = f"{from_link_id}-{to_link_id}"
                            if new_conn_id not in connectors_data_:
                                connectors_data_[new_conn_id] = {
                                    "from_lane_numbers": [],
                                    "to_lane_numbers": []
                                }

                            from_from_lane_numbers = connectors_data_[from_conn_id]["from_lane_numbers"]
                            from_to_lane_numbers = connectors_data_[from_conn_id]["to_lane_numbers"]
                            to_from_lane_numbers = connectors_data_[to_conn_id]["from_lane_numbers"]
                            to_to_lane_numbers = connectors_data_[to_conn_id]["to_lane_numbers"]

                            from_this_mapping = {}
                            for from_lane_number, to_lane_number in zip(from_from_lane_numbers, from_to_lane_numbers):
                                if from_lane_number not in from_this_mapping:
                                    from_this_mapping[from_lane_number] = []
                                from_this_mapping[from_lane_number].append(to_lane_number)

                            this_to_mapping = {}
                            for from_lane_number, to_lane_number in zip(to_from_lane_numbers, to_to_lane_numbers):
                                if from_lane_number not in this_to_mapping:
                                    this_to_mapping[from_lane_number] = []
                                this_to_mapping[from_lane_number].append(to_lane_number)

                            for from_lane_number, from_lane_numbers in from_this_mapping.items():
                                for lane_number in from_lane_numbers:
                                    if lane_number in this_to_mapping:
                                        to_lane_numbers = this_to_mapping[lane_number]
                                        for to_lane_number in to_lane_numbers:
                                            connectors_data_[new_conn_id]["from_lane_numbers"].append(from_lane_number)
                                            connectors_data_[new_conn_id]["to_lane_numbers"].append(to_lane_number)
                                            connectors_data_[new_conn_id]["from_lane_numbers"].sort()
                                            connectors_data_[new_conn_id]["to_lane_numbers"].sort()

                            # 更新上游路段的 to_link_and_conn
                            if [link_id, from_conn_id] in links_data_[from_link_id]["to_link_and_conn"]:
                                links_data_[from_link_id]["to_link_and_conn"].remove([link_id, from_conn_id])
                            if [to_link_id, new_conn_id] not in links_data_[from_link_id]["to_link_and_conn"]:
                                links_data_[from_link_id]["to_link_and_conn"].append([to_link_id, new_conn_id])
                            # 更新下游路段的 from_link_and_conn
                            if [link_id, to_conn_id] in links_data_[to_link_id]["from_link_and_conn"]:
                                links_data_[to_link_id]["from_link_and_conn"].remove([link_id, to_conn_id])
                            if [from_link_id, new_conn_id] not in links_data_[to_link_id]["from_link_and_conn"]:
                                links_data_[to_link_id]["from_link_and_conn"].append([from_link_id, new_conn_id])

                    # 删除上游连接段
                    for _, from_conn_id in from_link_and_conn:
                        connectors_data_.pop(from_conn_id)
                    # 删除下游连接段
                    for _, to_conn_id in to_link_and_conn:
                        connectors_data_.pop(to_conn_id)
                    # 删除本路段
                    links_data_.pop(link_id)

        # # 合并路段
        # def _merge_links(links_data_: dict, connectors_data_: dict) -> None:
        #     for link_id, link in links_data_.copy().items():
        #         to_link = link["to_link_and_conn"]
        #         # 如果本路段下游只有一个路段
        #         if len(to_link) == 1:
        #             this_lane_coount = len(link["lanes_width"])
        #             to_link_id, to_conn_id = to_link[0]
        #             to_lane_count = len(links_data_[to_link_id]["lanes_width"])
        #             # 如果本路段与下游路段的车道数相同
        #             if this_lane_coount == to_lane_count:
        #                 # 删除连接段
        #                 connectors_data_.pop(to_conn_id)
        #                 # 更新下游路段数据：points、from_link_and_conn
        #                 this_link_length = link["link_length"]
        #                 to_link_length = links_data_[to_link_id]["link_length"]
        #                 # 去掉可能多余的点
        #                 length_threshold = 1  # m
        #                 if this_link_length < length_threshold or to_link_length < length_threshold:
        #                     links_data_[to_link_id]["link_points"] = link["link_points"][:-1] + links_data_[to_link_id]["link_points"][1:]
        #                 else:
        #                     links_data_[to_link_id]["link_points"] = link["link_points"] + links_data_[to_link_id]["link_points"]
        #                 links_data_[to_link_id]["link_length"] = this_link_length + to_link_length + 0.5
        #                 links_data_[to_link_id]["from_link_and_conn"] = link["from_link_and_conn"]
        #                 # 更新上游连接段数据
        #                 from_link = link["from_link_and_conn"]
        #                 for _, from_conn_id in from_link:
        #                     conn_from_link_id, conn_to_link_id = from_conn_id.split("-")
        #                     conn_data = connectors_data_[from_conn_id]
        #                     new_conn_id = f"{conn_from_link_id}-{to_link_id}"
        #                     # 数据不变，创建新的连接段ID
        #                     connectors_data_[new_conn_id] = conn_data
        #                     # 删除原连接段ID
        #                     connectors_data_.pop(from_conn_id)
        #                 # 删除本路段
        #                 links_data_.pop(link_id)

        def _update_center_points(links_data: dict) -> None:
            xs, ys = [], []
            for link in links_data.values():
                points = link["link_points"]
                xs.extend([p[0] for p in points])
                ys.extend([p[1] for p in points])
            x_center = (min(xs) + max(xs)) / 2
            y_center = (min(ys) + max(ys)) / 2
            self.center_point = [x_center, y_center]

        links_data = _analyse_links(original_links_data)
        connectors_data = _analyse_connectors(original_connectors_data, links_data)
        _handle_narrow_lanes(links_data, connectors_data)
        _handle_short_links(links_data, connectors_data)
        _update_center_points(links_data)

        standard_links_data = [
            dict(
                id=link_id,
                points=link_data["link_points"],
                lanes_width=link_data["lanes_width"],
                name=link_data["link_name"],
            )
            for link_id, link_data in links_data.items()
        ]

        standard_connectors_data = [
            dict(
                from_link_id=connector_id.split("-")[0],
                to_link_id=connector_id.split("-")[1],
                from_lane_numbers=connector_data["from_lane_numbers"],
                to_lane_numbers=connector_data["to_lane_numbers"],
            )
            for connector_id, connector_data in connectors_data.items()
        ]

        return standard_links_data, standard_connectors_data

    # 解析车辆组成
    def analyse_vehicleCompositions(self, original_vehicleCompositions_data: dict) -> list:
        # 解析车辆组成
        standard_vehicleCompositions_data = []

        for vehicleComposition in pgd.progress(original_vehicleCompositions_data, "车辆组成数据解析中(5/12)"):
            vehicleComposition_id = vehicleComposition["no"]
            vehi_type_code_list = [
                self.vehiTypeCode_mapping.get(vehi_type_code, 1)
                for _, _, vehi_type_code in vehicleComposition["relativeFlows"]
            ]
            vehi_type_ratio_list = [
                ratio
                for _, ratio, _ in vehicleComposition["relativeFlows"]
            ]

            vehicleComposition_data = dict(
                id=str(vehicleComposition_id),
                vehi_type_code_list=vehi_type_code_list,
                vehi_type_ratio_list=vehi_type_ratio_list,
            )
            standard_vehicleCompositions_data.append(vehicleComposition_data)

        return standard_vehicleCompositions_data

    # 解析车辆输入
    def analyse_vehicleInputs(self, original_vehicleInputs_data: dict) -> list:
        standard_vehicleInputs_data = []

        for vehicleInput in pgd.progress(original_vehicleInputs_data, "车辆输入数据解析中(6/12)"):
            vehicleInput_id = vehicleInput["no"]
            link_id = vehicleInput["link"]
            vehicle_compose_id = vehicleInput["vehComp"]
            volume = int(vehicleInput["volume"] * self.valid_duration/3600)

            vehicleInput_data = dict(
                id=str(vehicleInput_id),
                link_id=str(link_id),
                vehicle_compose_id=str(vehicle_compose_id),
                volumes=[volume],
                durations=[self.valid_duration],
            )
            standard_vehicleInputs_data.append(vehicleInput_data)

        return standard_vehicleInputs_data

    # 解析信号灯组及相位
    def analyse_signalGroups(self, original_signalGroups_data: dict) -> list:
        signalGroups_data = []

        for signalGroup in pgd.progress([original_signalGroups_data], "信号灯组及相位数据解析中(7/12)"):
            signalGroup_id = 1
            cycletime = signalGroup[0]["cycletime"]
            signalGroup_data = dict(
                id=str(signalGroup_id),
                cycletime=cycletime,
                phases=[],
                duration=self.valid_duration,
            )
            for phase in signalGroup:
                phase_id = phase["sg_id"]
                colors = ["红", "绿", "黄", "红"]
                green_start_time = phase["greenStartTime"]
                green_end_time = phase["greenEndTime"]
                durations = [
                    end_time - start_time
                    for start_time, end_time in zip(
                        [0, green_start_time, green_end_time - 3, green_end_time],
                        [green_start_time, green_end_time - 3, green_end_time, cycletime]
                    )
                ]
                phase_data = dict(
                    id=str(phase_id),
                    colors=colors,
                    durations=durations,
                )
                signalGroup_data["phases"].append(phase_data)
            signalGroups_data.append(signalGroup_data)

        return signalGroups_data

    # 解析信号灯头
    def analyse_signalHeads(self, original_signalHeads_data: dict) -> list:
        signalHeads_data = []

        for signalHead in pgd.progress(original_signalHeads_data, "信号灯头数据解析中(8/12)"):
            signalHead_id = signalHead["no"]
            phase_id = signalHead["sg"][1]
            link_id, lane_number, dist = signalHead["lanePt"]
            signalHead_data = dict(
                id=str(signalHead_id),
                phase_id=str(phase_id),
                link_id=str(link_id),
                lane_number=int(lane_number),
                dist=float(dist),
            )
            signalHeads_data.append(signalHead_data)

        return signalHeads_data

    # 解析决策点
    def analyse_decisionPoints(self, original_decisionPoints_data: dict) -> list:
        decisionPoints_data = []

        for decisionPoint in pgd.progress(original_decisionPoints_data, "决策点和决策路径数据解析中(9/12)"):
            decisionPoint_id = decisionPoint["no"]
            link_id = decisionPoint["link"]
            pos = decisionPoint["pos"]
            routings = [
                [str(link_id) for link_id in [link_id] + value["linkSeq"] + [str(value["destLink"])]]
                for value in decisionPoint["vehicleRouteStatics"]
            ]
            ratios = [
                float(value["relFlow"])
                for value in decisionPoint["vehicleRouteStatics"]
            ]
            decisionPoint_data = dict(
                id=str(decisionPoint_id),
                link_id=str(link_id),
                dist=float(pos),
                routings=routings,
                ratios=ratios,
                duration=self.valid_duration,
            )
            decisionPoints_data.append(decisionPoint_data)

        return decisionPoints_data

    # 解析减速区
    def analyse_reducedSpeedAreas(self, original_reducedSpeedAreas_data: dict) -> list:
        reducedSpeedAreas_data = []

        for reducedSpeedArea in pgd.progress(original_reducedSpeedAreas_data, "减速区数据解析中(10/12)"):
            reducedSpeedArea_id = reducedSpeedArea["no"]
            speed = reducedSpeedArea["speed"]  # km/h
            link_id, lane_number, dist = reducedSpeedArea["lanePt"]
            length = reducedSpeedArea["len"]
            reducedSpeedArea_data = dict(
                id=str(reducedSpeedArea_id),
                link_id=str(link_id),
                lane_number=int(lane_number),
                dist=float(dist),
                length=float(length),
                speed=float(speed),
                to_time=self.valid_duration,
            )
            reducedSpeedAreas_data.append(reducedSpeedArea_data)

        return reducedSpeedAreas_data
