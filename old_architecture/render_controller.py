from typing import Iterable
import pygame
import color
from requirements import GameObject, Renderer


class RenderController:
    def __init__(
        self,
        resolution: tuple[int, int],
        background_image: pygame.surface.Surface | None = None,
    ) -> None:
        """Initialize the render controller

        Args:
            resolution (tuple[int, int]): Screen resolution
            background_image (None | pygame.surface.Surface, optional): An image for the
            background. Defaults to None.
        """
        self._resolution = resolution
        self.resize_main_screen()
        self._background_image = background_image
        self._background_color = color.BLACK
        self._renderers: dict[str, Renderer] = {}

    def register_renderer(self, object_type: str, renderer: Renderer) -> None:
        self._renderers[object_type] = renderer

    def unregister_renderer(self, object_type: str) -> None:
        if object_type in self._renderers:
            del self._renderers[object_type]

    def render(self, game_objects: Iterable[GameObject]) -> None:
        """Paint all the game objects on the screen

        Args:
            game_objects (list[GameObject]): _description_
        """
        self.clear_screen()
        for game_object in game_objects:
            renderer = self._renderers.get(game_object.get_type())
            if renderer:
                renderer.draw(self._main_screen, game_object)
        pygame.display.update()

    def resize_main_screen(self) -> None:
        """Resize the main screen"""
        self._main_screen = pygame.display.set_mode(self._resolution)

    def set_resolution(self, resolution: tuple[int, int]) -> None:
        self._resolution = resolution

    def get_resolution(self) -> tuple[int, int]:
        return self._resolution

    def set_background_color(self, color: pygame.color.Color) -> None:
        self._background_color = color

    def set_background_image(self, image: pygame.surface.Surface) -> None:
        self._background_image = image

    def clear_screen(self) -> None:
        """Clear the screen by filling the screen with a specified color or draw the background
        image on it"""
        if self._background_image is None:
            self._main_screen.fill(self._background_color)
            return
        self._main_screen.blit(self._background_image, (0, 0))
