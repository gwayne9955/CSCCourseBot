from enum import Enum, auto


class Signal(Enum):
    NORMAL = auto()
    UNKNOWN = auto()
    QUESTION = auto()
    END = auto()
    ERROR = auto()
