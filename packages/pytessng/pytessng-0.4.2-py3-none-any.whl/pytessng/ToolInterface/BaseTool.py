from abc import ABC
from typing import Callable

from PySide2.QtCore import QPointF
from PySide2.QtGui import QVector3D
from pytessng.DLLs.Tessng import Online, _DecisionPoint, _RoutingFLowRatio


class BaseTool(ABC):
    def __init__(self, netiface=None, extension: bool = False):
        self.netiface = netiface
        self.scene_scale = netiface.sceneScale() if netiface else 1

        self.Online = Online if extension else None
        self.private_class = {
            "_DecisionPoint": _DecisionPoint,
            "_RoutingFLowRatio": _RoutingFLowRatio,
        } if extension else None

    def _p2m(self, x: float) -> float:
        return x * self.scene_scale

    def _m2p(self, x: float) -> float:
        return x / self.scene_scale

    def _qtpoint2list(self, qtpoints: list, move: dict = None) -> list:
        x_move, y_move = (0, 0) if move is None else (-move["x_move"], -move["y_move"])

        if type(qtpoints[0]) == QPointF:
            return [
                [
                    self._p2m(qt_point.x()) + x_move,
                    -self._p2m(qt_point.y()) + y_move,
                ]
                for qt_point in qtpoints
            ]
        return [
            [
                self._p2m(qt_point.x()) + x_move,
                -self._p2m(qt_point.y()) + y_move,
                self._p2m(qt_point.z())
            ]
            for qt_point in qtpoints
        ]

    def _list2qtpoint(self, points, move: dict = None) -> list:
        if len(points) < 2:
            raise Exception("The length of points is not valid!")

        x_move, y_move = (0, 0) if move is None else (move["x_move"], move["y_move"])

        if len(points[0]) == 2:
            return [
                QPointF(
                    self._m2p(float(point[0])) + x_move,
                    -(self._m2p(float(point[1])) + y_move),
                )
                for point in points
            ]
        else:
            return [
                QVector3D(
                    self._m2p(float(point[0])) + x_move,
                    -(self._m2p(float(point[1])) + y_move),
                    self._m2p(float(point[2])),
                ) for point in points
            ]

    def _xy2lonlat(self, points: list, proj: Callable) -> list:
        if len(points[0]) == 2:
            return [
                [*proj(point[0], point[1], inverse=True)]
                for point in points
            ]
        else:
            return [
                [*proj(point[0], point[1], inverse=True), point[2]]
                for point in points
            ]
