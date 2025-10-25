from dataclasses import dataclass
from ecs.component import Component


@dataclass
class Transform(Component):
    position: tuple[float, float] = (0.0, 0.0)
    rotation: float = 0.0  # In degrees
    scale: tuple[float, float] = (1.0, 1.0)
