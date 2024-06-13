from PySide2.QtCore import QPointF

from ..BaseLinkEditor import BaseLinkEditor
from pytessng.Logger import logger


class NetworkMover(BaseLinkEditor):
    def edit(self, move_to_center: bool, x_move: float, y_move: float) -> None:
        # 移动路网
        links = self.netiface.links()

        if move_to_center:
            # 计算路网中心点
            xs, ys = [], []
            for link in links:
                points = self._qtpoint2list(link.centerBreakPoint3Ds())
                xs.extend([p[0] for p in points])
                ys.extend([p[1] for p in points])
            x_center, y_center = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
            x_move, y_move = -x_center, -y_center

        move = QPointF(self._m2p(x_move), -self._m2p(y_move))
        self.netiface.moveLinks(links, move)

        logger.logger_pytessng.info(f"移动路网：[横向距离为{x_move:.2f}m] [纵向距离为{y_move:.2f}m]")

        # 更新场景大小
        x_max, y_max = 300, 200
        for link in links:
            points = self._qtpoint2list(link.centerBreakPoint3Ds())
            xs = [abs(p[0]) for p in points]
            ys = [abs(p[1]) for p in points]
            x_max = max(x_max, max(xs))
            y_max = max(y_max, max(ys))
        self.netiface.setSceneSize(x_max * 2 + 20, y_max * 2 + 20)
