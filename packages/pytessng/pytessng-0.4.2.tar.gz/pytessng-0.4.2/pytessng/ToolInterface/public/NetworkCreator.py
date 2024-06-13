import traceback

from ..BaseTool import BaseTool
from .DataClass import Attrs, Link, Connector, VehicleComposition, VehicleInput
from .DataClass import SignalPhase, SignalGroup, SignalHead, DecisionPoint, ReducedSpeedArea
from pytessng.Logger import logger
from pytessng.ProgressDialog import ProgressDialogClass as pgd


class NetworkCreator(BaseTool):
    def __init__(self, netiface, move: dict = None, pgd_index: tuple = (1, 2)):
        super().__init__(netiface, extension=True)
        # move
        self.move = move if move else {"x_move": 0, "y_move": 0}
        # 进度条相关
        self.pgd_index_start = pgd_index[0]
        self.pgd_index_max = pgd_index[1]

        # 路段ID映射字典
        self.link_id_mapping = {}
        # 车辆组成ID映射字典
        self.vehicleCompositions_mapping = {}
        # 信号相位ID映射字典
        self.signalPhases_mapping = {}

        # 对象创建函数映射
        self.objects_mapping = {
            "links": self.create_links,
            "connectors": self.create_connectors,
            "vehicleCompositions": self.create_vehicleCompositions,
            "vehicleInputs": self.create_vehicleInputs,
            "signalGroups": self.create_signalGroups,
            "signalHeads": self.create_signalHeads,
            "decisionPoints": self.create_decisionPoints,
            "reducedSpeedAreas": self.create_reducedSpeedAreas,
        }

    # 设置路网属性
    def set_attrs(self, source: str, attrs: dict):
        # 构建对象
        attrs: Attrs = Attrs(**attrs)
        # 设置属性
        self.netiface.setNetAttrs(f"{source} Network", otherAttrsJson=attrs.dict())

    # 创建路网
    def create_network(self, network_data: dict) -> dict:
        result_create_network = dict()
        # 创建路网
        for object_type, objects_data in network_data.items():
            create_func = self.objects_mapping.get(object_type)
            if create_func:
                result_create_objects = create_func(objects_data)
                result_create_network[object_type] = result_create_objects
            else:
                logger.logger_pytessng.error(f"Failed to find the function of create {object_type}!")
                result_create_network[object_type] = None
        return result_create_network

    # 创建路段
    def create_links(self, links_data: list) -> dict:
        result_create = {}

        for link_data in pgd.progress(links_data, f"路段创建中({self.pgd_index_start}/{self.pgd_index_max})"):
            # 构建路段对象
            link = Link(**link_data)

            link_id = link.id
            points = link.points
            lane_count = link.lane_count
            lanes_width = [self._m2p(width) for width in link.lanes_width]
            lanes_points = link.lanes_points
            lanes_type = link.lanes_type
            limit_speed = self._m2p(link.limit_speed)
            name = link.name

            point_value_num = len(points[0])
            points = self._list2qtpoint(points, self.move)

            try:
                # 用车道点位
                if lanes_points:
                    for lane_point in lanes_points:
                        for location in ["left", "center", "right"]:
                            lane_point[location] = self._list2qtpoint(lane_point[location], self.move)
                    link_obj = self.netiface.createLink3DWithLanePoints(points, lanes_points, name)
                # 用车道宽度
                elif lanes_width:
                    if point_value_num == 2:
                        link_obj = self.netiface.createLinkWithLaneWidth(points, lanes_width, name)
                    else:
                        link_obj = self.netiface.createLink3DWithLaneWidth(points, lanes_width, name)
                # 用车道数量
                else:
                    if point_value_num == 2:
                        link_obj = self.netiface.createLink(points, lane_count, name)
                    else:
                        link_obj = self.netiface.createLink3D(points, lane_count, name)

                # 如果创建成功，设置限速和车道类型
                if link_obj:
                    # 限速
                    if limit_speed:
                        link_obj.setLimitSpeed(limit_speed)
                    # 车道类型
                    for lane, lane_type in zip(link_obj.lanes(), lanes_type):
                        lane.setLaneType(lane_type)
                    # 保存对应关系
                    self.link_id_mapping[link_id] = link_obj.id()
                    result_create[link_id] = link_obj.id()
                else:
                    self.handle_error("Link", link_id, result_create)

            except:
                self.handle_error("Link", link_id, result_create, traceback.format_exc())

        # 更新场景尺寸
        self.update_scene_size()

        return result_create

    # 创建连接段
    def create_connectors(self, connectors_data: list) -> dict:
        result_create = {}

        for connector_data in pgd.progress(connectors_data, f"连接段创建中({self.pgd_index_start + 1}/{self.pgd_index_max})"):
            # 构建连接段对象
            connector = Connector(**connector_data)

            from_link_id = self.link_id_mapping.get(connector.from_link_id, connector.from_link_id)
            to_link_id = self.link_id_mapping.get(connector.to_link_id, connector.to_link_id)
            from_lane_numbers = connector.from_lane_numbers
            to_lane_numbers = connector.to_lane_numbers
            lanes_points = None  # connector.lanes_points  # TODO: 暂时不支持

            connector_id = f"{from_link_id}-{to_link_id}"

            try:
                from_link_id = int(from_link_id)
                to_link_id = int(to_link_id)

                # 不给点位
                if not lanes_points:
                    connector = self.netiface.createConnector(from_link_id, to_link_id, from_lane_numbers, to_lane_numbers)
                # 给点位
                else:
                    for lane_point in lanes_points:
                        for location in ["left", "center", "right"]:
                            lane_point[location] = self._list2qtpoint(lane_point[location])
                    connector = self.netiface.createConnector(from_link_id, to_link_id, from_lane_numbers, to_lane_numbers, lanes_points)

                # 如果创建成功
                if connector:
                    # 保存对应关系
                    result_create[connector_id] = connector.id()
                else:
                    self.handle_error("Connector", connector_id, result_create)
            except:
                self.handle_error("Connector", connector_id, result_create, traceback.format_exc())

        return result_create

    # 创建车辆组成
    def create_vehicleCompositions(self, vehicleCompositions_data: list) -> dict:
        result_create = {}

        for vehicleComposition_data in vehicleCompositions_data:
            # 构建车辆组成对象
            vehicleComposition = VehicleComposition(**vehicleComposition_data)

            vehicle_composition_id = vehicleComposition.id
            vehicle_composition_name = vehicleComposition.id
            vehi_type_code_list = vehicleComposition.vehi_type_code_list
            vehi_type_ratio_list = vehicleComposition.vehi_type_ratio_list
            try:
                vehicle_data_list = [
                    self.Online.VehiComposition(vehi_type_code, vehi_type_ratio)
                    for vehi_type_code, vehi_type_ratio in zip(vehi_type_code_list, vehi_type_ratio_list)
                ]
                vehicleComposition_actual_id = self.netiface.createVehicleComposition(vehicle_composition_name, vehicle_data_list)

                # 如果创建成功
                if vehicleComposition_actual_id:
                    # 保存对应关系
                    result_create[vehicle_composition_id] = vehicleComposition_actual_id
                else:
                    self.handle_error("vehicleComposition", vehicle_composition_id, result_create)
            except:
                self.handle_error("VehicleComposition", vehicle_composition_id, result_create, traceback.format_exc())

        return result_create

    # 创建发车点
    def create_vehicleInputs(self, vehicleInputs_data: list) -> dict:
        result_create = {}

        for vehicleInput_data in vehicleInputs_data:
            # 构建发车点对象
            vehicleInput = VehicleInput(**vehicleInput_data)

            vehicle_input_id = vehicleInput.id
            vehicle_input_name = vehicle_input_id
            vehicle_compose_id = self.vehicleCompositions_mapping.get(vehicleInput.vehicle_compose_id, vehicleInput.vehicle_compose_id)
            link_id = self.link_id_mapping.get(vehicleInput.link_id, vehicleInput.link_id)
            volumes = vehicleInput.volumes
            durations = vehicleInput.durations
            try:
                link = self.netiface.findLink(link_id)
                if link:
                    dp = self.netiface.createDispatchPoint(link, dpName=vehicle_input_name)
                    if dp:
                        for volume, duration in zip(volumes, durations):
                            dp.addDispatchInterval(int(vehicle_compose_id), duration, volume)  # 车辆组成、时间间隔、车辆数
                        result_create[vehicle_input_id] = dp.id()
                    else:
                        self.handle_error("VehicleInput", vehicle_input_id, result_create, f"No find Link {link_id}!")
                else:
                    self.handle_error("VehicleInput", vehicle_input_id, result_create)
            except:
                self.handle_error("VehicleInput", vehicle_input_id, result_create, traceback.format_exc())

        return result_create

    # 创建信号灯组及相位
    def create_signalGroups(self, signalGroups_data: list) -> dict:
        result_create = {}

        for signalGroup_data in signalGroups_data:
            # 构建信号相位对象
            signalGroup_data["phases"] = [
                SignalPhase(**phase_data)
                for phase_data in signalGroup_data["phases"]
            ]
            # 构建信号灯组对象
            signalGroup = SignalGroup(**signalGroup_data)

            signal_group_id = signalGroup.id
            signal_group_name = signal_group_id
            cycletime = signalGroup.cycletime  # 周期时间
            phases = signalGroup.phases  # 相位
            duration = signalGroup.duration  # 持续时间
            try:
                signal_group = self.netiface.createSignalGroup(signal_group_name, cycletime, 0, duration)
                # 创建信号相位
                for phase in phases:
                    phase_id = phase.id
                    phase_name = phase_id
                    colors = phase.colors
                    durations = phase.durations
                    try:
                        signal_phase = [
                            self.Online.ColorInterval(color, duration)
                            for color, duration in zip(colors, durations)
                        ]
                        signalPhase = self.netiface.createSignalPhase(signal_group, phase_name, signal_phase)

                        # 如果创建成功
                        if signalPhase:
                            self.signalPhases_mapping[phase_id] = signalPhase.id()
                            result_create[phase_id] = signalPhase.id()
                        else:
                            self.handle_error("SignalPhase", phase_id, result_create)
                    except:
                        self.handle_error("SignalPhase", phase_id, result_create, traceback.format_exc())
            except:
                self.handle_error("SignalGroup", signal_group_id, result_create, traceback.format_exc())

        return result_create

    # 创建信号灯头
    def create_signalHeads(self, signalHeads_data: list) -> dict:
        result_create = {}

        for signalHead_data in signalHeads_data:
            # 构建信号灯头对象
            signalHead = SignalHead(**signalHead_data)

            signal_head_id = signalHead.id
            signal_head_name = str(signal_head_id)
            phase_id = self.signalPhases_mapping.get(signalHead.phase_id, signalHead.phase_id)
            link_id = self.link_id_mapping.get(signalHead.link_id, signalHead.link_id)
            dist = self._m2p(signalHead.dist)
            lane_numer = signalHead.lane_number
            try:
                signalPhase = self.netiface.findSignalPhase(phase_id)
                link = self.netiface.findLink(link_id)
                lane = [lane for i, lane in enumerate(link.lanes()) if i + 1 == lane_numer]
                lane_id = lane[0].id()
                signalLamp = self.netiface.createSignalLamp(signalPhase, signal_head_name, lane_id, 0, dist)

                # 如果创建成功
                if signalLamp:
                    result_create[signal_head_id] = signalLamp.id()
                else:
                    self.handle_error("SignalPhase", signal_head_id, result_create)
            except:
                self.handle_error("SignalPhase", signal_head_id, result_create, traceback.format_exc())

        return result_create

    # 创建决策点
    def create_decisionPoints(self, decisionPoints_data: list) -> dict:
        result_create = {}

        _DecisionPoint = self.private_class["_DecisionPoint"]
        _RoutingFLowRatio = self.private_class["_RoutingFLowRatio"]

        # 更新决策点添加路径
        def _update_decisionPoint(decisionPoint_id_: int, hour_: int, routings_flow: dict):
            decisionPoint = _DecisionPoint()
            decisionPoint.deciPointID = decisionPoint_id_
            decisionPoint.deciPointName = f"{decisionPoint_id_}"
            decisionPoint.X = 0
            decisionPoint.Y = 0
            decisionPoint.Z = 0

            ratio_data = []
            for routing_id_, flow_ in routings_flow.items():
                r = _RoutingFLowRatio()
                r.startDateTime = 0
                r.endDateTime = 3600 * hour_
                r.ratio = flow_
                r.routingID = routing_id_
                ratio_data.append(r)

            decisionPoint = self.netiface.updateDecipointPoint(decisionPoint, ratio_data)
            return decisionPoint

        for decisionPoint_data in decisionPoints_data:
            # 构建决策点对象
            decisionPoint = DecisionPoint(**decisionPoint_data)

            decision_point_id = decisionPoint.id
            decision_point_name = decision_point_id
            link_id = self.link_id_mapping.get(decisionPoint.link_id, decisionPoint.link_id)
            dist = self._m2p(decisionPoint.dist)
            routings = decisionPoint.routings
            ratios = decisionPoint.ratios
            duration = decisionPoint.duration
            try:
                link = self.netiface.findLink(link_id)
                # 创建决策点
                decisionPoint = self.netiface.createDecisionPoint(link, dist, decision_point_name)
                decisionPoint_id = decisionPoint.id()
                routings_flow = {}
                # 创建决策路径
                for routing, ratio in zip(routings, ratios):
                    routing_ = [
                        self.netiface.findLink(int(self.link_id_mapping[link_id]))
                        for link_id in routing
                        if link_id in self.link_id_mapping
                    ]
                    routing_object = self.netiface.createDeciRouting(decisionPoint, routing_)
                    routing_id = routing_object.id()
                    routings_flow[routing_id] = ratio
                # 更新路径流量
                decisionPoint = _update_decisionPoint(decisionPoint_id, duration, routings_flow)

                # 如果创建成功
                if decisionPoint:
                    result_create[decision_point_id] = decisionPoint_id
                else:
                    self.handle_error("DecisionPoint", decision_point_id, result_create)
            except:
                self.handle_error("DecisionPoint", decision_point_id, result_create, traceback.format_exc())

        return result_create

    # 创建减速区
    def create_reducedSpeedAreas(self, reducedSpeedAreas_data: list) -> dict:
        result_create = {}

        SPEED_STANDARD_DEVIATION = 1

        def _get_reduceSpeedVehicleType_list(speed):
            reduceSpeedVehicleType_list = []
            for vehicleTypeCode in range(1, 12):
                rsvt = self.Online.ReduceSpeedVehicleType()
                rsvt.avgSpeed = speed
                rsvt.speedSD = SPEED_STANDARD_DEVIATION
                rsvt.vehicleTypeCode = vehicleTypeCode
                reduceSpeedVehicleType_list.append(rsvt)
            return reduceSpeedVehicleType_list

        for reducedSpeedArea_data in reducedSpeedAreas_data:
            # 构建减速区对象
            reducedSpeedArea = ReducedSpeedArea(**reducedSpeedArea_data)

            reduced_speed_area_id = reducedSpeedArea.id
            reduced_speed_area_name = reduced_speed_area_id
            speed = self._m2p(reducedSpeedArea.speed)
            link_id = self.link_id_mapping.get(reducedSpeedArea.link_id, reducedSpeedArea.link_id)
            lane_number = reducedSpeedArea.lane_number
            dist = self._m2p(reducedSpeedArea.dist)
            length = self._m2p(reducedSpeedArea.length)
            to_time = reducedSpeedArea.to_time
            reduceSpeedVehicleType_list = _get_reduceSpeedVehicleType_list(speed)
            try:
                reduceSpeedArea = self.netiface.createReduceSpeedArea(reduced_speed_area_name, dist, length, link_id, lane_number, -1, 0, to_time, reduceSpeedVehicleType_list)

                # 如果创建成功
                if reduceSpeedArea:
                    result_create[reduced_speed_area_id] = reduceSpeedArea.id()
                else:
                    self.handle_error("ReduceSpeedArea", reduced_speed_area_id, result_create)
            except:
                self.handle_error("ReduceSpeedArea", reduced_speed_area_id, result_create, traceback.format_exc())

        return result_create

    # 更新场景尺寸
    def update_scene_size(self) -> None:
        scene_size = [300, 200]

        all_links = self.netiface.links()
        if all_links:
            xs, ys = [], []
            for link in all_links:
                points = self._qtpoint2list(link.centerBreakPoints())
                xs.extend([point[0] for point in points])
                ys.extend([point[1] for point in points])

                scene_size[0] = max(scene_size[0], max(xs))
                scene_size[1] = max(scene_size[1], max(ys))

        width = scene_size[0] * 2 + 10
        height = scene_size[1] * 2 + 10
        self.netiface.setSceneSize(width, height)  # m

    # 错误处理
    def handle_error(self, object_name: str, object_id: str, result_create: dict, error_message: str = None) -> None:
        logger.logger_pytessng.error(f"Failed to create {object_name} {object_id}!")
        if error_message:
            logger.logger_pytessng.error(error_message)
        result_create[object_id] = None
