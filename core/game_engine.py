import pygame
from core.render_controller import RenderController
from core.game_object_manager import GameObjectManager
from core.event_manager import EventManager
from abc import ABC, abstractmethod


class Game(ABC):
    def __init__(
        self,
        resolution: tuple[int, int] = (640, 480),
        fps: int = 60,
        caption: str = "Game",
    ) -> None:
        """Initialize the game

        Args:
            resolution (tuple[int, int], optional): Screen resolution. Defaults to (640, 480).
            fps (int, optional): Screen refresh rate(frames per second). Defaults to 60.
            caption (str, optional): Window's caption. Defaults to "Game".
        """
        pygame.init()
        self._clock = pygame.time.Clock()
        self.set_fps(fps)
        self.set_caption(caption)
        self.render_controller = RenderController(resolution)
        self.game_object_manager = GameObjectManager()
        self.event_manager = EventManager()

    def set_fps(self, fps: int) -> None:
        self._fps = fps
        self._frame_time = 1 / fps

    def set_caption(self, caption: str) -> None:
        self._caption = caption
        pygame.display.set_caption(self._caption)

    def draw_screen(self) -> None:
        """Draw visible objects on the screen at specified FPS"""
        self.render_controller.render(self.game_object_manager.get_all())
        self._clock.tick(self._fps)

    @abstractmethod
    def update(self) -> None:
        """Call update for all game object. Overrides this method to update game object state
        outside of the game object manager"""
        for game_object in self.game_object_manager.get_all():
            game_object.update(
                self.render_controller.get_resolution(), self._frame_time
            )

    @abstractmethod
    def run(self) -> None:
        """Override this method to run the game loop"""
        pass


def main() -> None:
    pass


if __name__ == "__main__":
    main()
