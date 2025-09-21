from typing import Generic, Protocol, TypeVar
import pygame


class GameObject(Protocol):
    def update(self, resolution: tuple[int, int], time_step: float) -> None: ...

    def get_type(self) -> str: ...


T = TypeVar("T", bound=GameObject, contravariant=True)


class Renderer(Protocol, Generic[T]):

    def draw(self, screen: pygame.surface.Surface, obj: T) -> None: ...
