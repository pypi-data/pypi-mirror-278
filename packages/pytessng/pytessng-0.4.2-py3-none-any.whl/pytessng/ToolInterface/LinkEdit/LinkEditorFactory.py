from .LinkCreator.LinkCreator import LinkCreator
from .LinkLocator.LinkLocator import LinkLocator
from .LinkSplitter.LinkSplitter import LinkSplitter
from .LinkMerger.LinkMerger import LinkMerger
from .LinkSimplifier.LinkSimplifier import LinkSimplifier
from .ConnectorLengthLimiter.ConnectorLengthLimiter import ConnectorLengthLimiter
from .LinkLengthLimiter.LinkLengthLimiter import LinkLengthLimiter
from .LinkLimitSpeedModifier.LinkLimitSpeedModifier import LinkLimitSpeedModifier
from .NetworkMover.NetworkMover import NetworkMover


class LinkEditorFactory:
    mode_mapping = {
        "create": LinkCreator,  # lane_count: int, lane_width: float, lane_points: str
        "locate": LinkLocator,  # pos: QPointF
        "split": LinkSplitter,  # link_id: int, pos: QPointF, min_connector_length: float = xxx
        "merge": LinkMerger,  # include_connector: bool = xxx, simplify_points: bool = xxx
        "simplify": LinkSimplifier,  # max_distance: float = xxx, max_length: float = xxx
        "limit_c": ConnectorLengthLimiter,  # min_connector_length: float = xxx
        "limit_l": LinkLengthLimiter,  # max_length_length: float = xxx, min_connector_length: float = xxx
        "modify": LinkLimitSpeedModifier,  # limit_speed: float
        "move": NetworkMover,  # move_to_center: bool, x_move: float, y_move: float
    }

    @classmethod
    def build(cls, mode: str, netiface, params: dict):
        if mode in cls.mode_mapping:
            model = cls.mode_mapping[mode](netiface)
            return model.edit(**params)
        else:
            raise Exception("No This Export Mode!")
