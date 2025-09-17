from typing import Protocol
import pygame


class GameObject(Protocol):
    def draw(self, screen: pygame.surface.Surface) -> None:
        ...

    def update(self, resolution: tuple[int, int], time_step: float) -> None:
        ...
