from enum import Enum, auto


class RobotEnum(Enum):
    """
    Enum for robot types. Choose the robot type you want to use.
    """
    GEN3_LITE = auto()
    NED = auto()
    GEN3 = auto()
    DUMMY = auto()
