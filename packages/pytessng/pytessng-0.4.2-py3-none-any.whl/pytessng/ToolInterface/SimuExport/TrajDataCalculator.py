import time
import math
from typing import Callable


class TrajDataCalculator:
    @staticmethod
    def get_basic_traj_data(simuiface, p2m: Callable = lambda x: x):
        # 当前已仿真时间，单位：毫秒
        simu_time = simuiface.simuTimeIntervalWithAcceMutiples()
        # 开始仿真的现实时间戳，单位：毫秒
        start_time = simuiface.startMSecsSinceEpoch()
        # 当前仿真计算批次
        batchNum = simuiface.batchNumber()
        # 当前正在运行车辆列表
        lAllVehi = simuiface.allVehiStarted()

        traj_data = {
            "timestamp": str(int(time.time() * 1000)),
            "simuTime": simu_time,
            'startSimuTime': start_time,
            "batchNum": batchNum,
            "count": len(lAllVehi),
            "objs": [],
        }

        for vehi in lAllVehi:
            x = p2m(vehi.pos().x())
            y = -p2m(vehi.pos().y())
            if math.isnan(x) or math.isnan(y):
                continue

            in_link = vehi.roadIsLink()

            # 车辆寻找异常，跳过
            if (in_link and not vehi.lane()) or (not in_link and not vehi.laneConnector()):
                continue

            lane = vehi.lane()
            angle = vehi.angle()
            veh_data = {
                "id": vehi.id(),
                'typeCode': vehi.vehicleTypeCode(),
                'roadId': vehi.roadId(),
                'inLink': in_link,
                'laneCount': in_link and lane.link().laneCount(),
                'laneNumber': in_link and lane.number(),
                'laneTypeName': in_link and lane.actionType(),
                'angle': angle,
                'speed': p2m(vehi.currSpeed()),
                'Speed': p2m(vehi.currSpeed()) * 3.6,
                'size': [p2m(vehi.length()), 2, 2],
                'color': "",
                'x': x,
                'y': y,
                'z': vehi.v3z(),
                'longitude': None,
                'latitude': None,
                'eulerX': -angle / 180 * math.pi + math.pi / 2,
                'eulerY': -angle / 180 * math.pi + math.pi / 2,
                'eulerZ': -angle / 180 * math.pi + math.pi / 2,
            }

            traj_data['objs'].append(veh_data)

        return traj_data

    @staticmethod
    def get_complete_traj_data(basic_traj_data, proj: Callable, move: dict):
        for veh in basic_traj_data['objs']:
            x, y = veh['x'], veh['y']
            lon, lat = proj(x + move["x_move"], y + move["y_move"], inverse=True)
            veh["longitude"], veh["latitude"] = lon, lat

    @staticmethod
    def get_traj_data(simuiface, p2m: Callable, proj: Callable, move: dict):
        traj_data = TrajDataCalculator.get_basic_traj_data(simuiface, p2m)
        TrajDataCalculator.get_complete_traj_data(traj_data, proj, move)
        return traj_data





def get_signal_color_data(simuiface, netiface):
    simu_time = simuiface.simuTimeIntervalWithAcceMutiples()  # ms

    signal_color_data = dict(
        timestamp=int(time.time() * 1000),
        simuTime=simu_time,
        data={}
    )

    signal_group_list = netiface.signalGroups()
    signal_phase_color_list = simuiface.getSignalPhasesColor()
    for signal_group in signal_group_list:
        group_name = signal_group.groupName()
        signal_color_data['data'][group_name] = {}

        signal_phase_list = signal_group.phases()
        for signal_phase in signal_phase_list:
            phase_name = signal_phase.phaseName()
            phase_id = signal_phase.id()
            signal_lamp_list = signal_phase.signalLamps()

            if len(signal_lamp_list) == 0:
                continue

            signal_color_data['data'][group_name][phase_name] = dict(
                curColor=signal_lamp_list[0].color(),
                lampColor=[],
                duration=[],
                countDown=None
            )

            countDown = -1
            for signal_phase_color in signal_phase_color_list:
                if signal_phase_color.phaseId == phase_id:
                    countDown = int((signal_phase_color.mrIntervalSetted - signal_phase_color.mrIntervalByNow) / 1000)
            signal_color_data['data'][group_name][phase_name]['countDown'] = min(countDown, 255)

            for color_interval in signal_phase.listColor():
                signal_color_data['data'][group_name][phase_name]['lampColor'].append(color_interval.color)
                signal_color_data['data'][group_name][phase_name]['duration'].append(color_interval.interval)

    return signal_color_data
