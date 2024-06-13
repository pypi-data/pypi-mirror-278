from ..BaseLinkEditor import BaseLinkEditor


class LinkCreator(BaseLinkEditor):
    def edit(self, lane_count: int, lane_width: float, lane_points: str) -> None:
        points = [
            point.split(",")
            for point in lane_points.split(";")
        ]
        lanes_width = [
            lane_width
            for _ in range(lane_count)
        ]

        links_data = [
            {
                'id': "new",
                'points': points,
                'lanes_width': lanes_width,
            }
        ]
        network_data = {"links": links_data}

        # 创建路段
        pgd_index = (1, 1)
        self.network_creator(
            self.netiface,
            pgd_index=pgd_index
        ).create_network(network_data)
