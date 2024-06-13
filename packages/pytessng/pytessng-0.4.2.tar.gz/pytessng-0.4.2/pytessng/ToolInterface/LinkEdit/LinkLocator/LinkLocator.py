from PySide2.QtCore import QPointF

from ..BaseLinkEditor import BaseLinkEditor
from pytessng.Config import LinkEditConfig


class LinkLocator(BaseLinkEditor):
    def edit(self, pos: QPointF) -> list:
        DIST = LinkEditConfig.Locator.DIST

        # 网格化
        self.netiface.buildNetGrid(5)

        # 找到一定距离之内的车道所在路段的ID
        all_link_id = []
        locations = self.netiface.locateOnCrid(pos, 9)
        for location in locations:
            dist = self._p2m(location.leastDist)
            lane = location.pLaneObject
            if dist < DIST and lane.isLane():
                link_id = int(lane.link().id())
                all_link_id.append(link_id)

        return sorted(set(all_link_id))
