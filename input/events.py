from enum import Enum, auto
from dataclasses import dataclass


class RawInputType(Enum):
    KEY_DOWN = auto()
    KEY_UP = auto()
    MOUSE_MOVE = auto()
    MOUSE_BUTTON_DOWN = auto()
    MOUSE_BUTTON_UP = auto()
    RESIZE = auto()
    QUIT = auto()


@dataclass(frozen=True)
class RawInputEvent:
    type: RawInputType
    data: dict[str, any]
