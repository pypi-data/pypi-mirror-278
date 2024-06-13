from .LineBase import LineBase


class PointsDivider:
    """ 分割路段 """
    @staticmethod
    def divide_line_by_distances(line: list, given_distance_list: list) -> (list, list):
        assert len(line) >= 2

        given_distance_list = sorted(given_distance_list)
        assert len(given_distance_list) > 0

        total_length = LineBase.calculate_line_length(line)
        assert given_distance_list[0] > 0 and given_distance_list[-1] < total_length

        all_length = 0
        all_points = [(line[0], False)]
        divide_infos = []
        last_index = -1
        index = 1
        k = 0

        while True:
            if index >= len(line):
                break

            p1, p2 = line[index - 1], line[index]
            dist = given_distance_list[k] if k < len(given_distance_list) else 1e6

            section_length = LineBase.calculate_two_points_distance(p1, p2)
            if index != last_index:
                all_length += section_length
                last_index = index

            if all_length < dist:
                if p2 not in [v[0] for v in all_points]:
                    all_points.append((p2, False))
                index += 1
            elif all_length == dist:
                all_points.append([p2, True])
                divide_infos.append([index, None])
                k += 1
            else:
                before_length = all_length - section_length
                ratio = round((dist - before_length) / section_length, 3)
                cut_point = LineBase.interpolate_point_on_segment(p1, p2, ratio)
                all_points.append([cut_point, True])
                divide_infos.append([index - 1, ratio])
                k += 1

        divided_points = [[], ]
        for p, flag in all_points:
            divided_points[-1].append(p)
            if flag:
                divided_points.append([p])

        return divided_points, divide_infos

    # 分隔线段
    @staticmethod
    def divide_line_by_indexes_and_ratios(line: list, split_infos: list) -> list:
        assert len(line) >= 2

        all_points = [(line[0], False)]
        i = 0
        k = 0
        while True:
            if k >= len(split_infos):
                all_points.append((line[-1], False))
                break

            index, ratio = split_infos[k]
            if index == i:
                p1 = line[index]
                p2 = line[index + 1]
                cut_point = LineBase.interpolate_point_on_segment(p1, p2, ratio)
                all_points.append((cut_point, True))
                k += 1
            else:
                if ratio is None:
                    all_points.append((line[index], True))
                    k += 1
                else:
                    all_points.append((line[index], False))
                i += 1

        divided_points = [[], ]
        for p, flag in all_points:
            divided_points[-1].append(p)
            if flag:
                divided_points.append([p])

        return divided_points


class LinkPointsDivider:
    @staticmethod
    def divide_link(points: list, lanes_points: list, given_distance_list: list) -> (list, list):
        # 分割的路段点位，分割信息
        divided_points, divide_infos = PointsDivider.divide_line_by_distances(points, given_distance_list)
        # 分隔的车道点位
        temp_lanes_points = [
            {
                "left": PointsDivider.divide_line_by_indexes_and_ratios(lane_points["left"], divide_infos),
                "center": PointsDivider.divide_line_by_indexes_and_ratios(lane_points["center"], divide_infos),
                "right": PointsDivider.divide_line_by_indexes_and_ratios(lane_points["right"], divide_infos),
            }
            for lane_points in lanes_points
        ]
        divided_lanes_points = [
            [
                {
                    "left": lane_points["left"][number],
                    "center": lane_points["center"][number],
                    "right": lane_points["right"][number],
                }
                for lane_points in temp_lanes_points
            ]
            for number in range(len(divided_points))
        ]

        return divided_points, divided_lanes_points
