from typing import Protocol
from enum import Enum, auto
from .target import RenderTarget


class RenderSpace(Enum):
    SCREEN = auto()
    WORLD = auto()


class RenderContext(Protocol):
    """Abstract renderer interface for all rendering backends."""

    def get_target(self) -> RenderTarget:
        """Get the current render target."""
        pass

    def set_target(self, target: RenderTarget) -> None:
        """Set the current render target."""
        pass

    def get_resolution(self) -> tuple[int, int]:
        """Get the current screen resolution."""
        pass

    def set_resolution(self, resolution: tuple[int, int]) -> None:
        """Set the screen resolution."""
        pass

    def start_frame(self) -> None:
        """Begin a new frame for rendering."""
        pass

    def end_frame(self) -> None:
        """End the current frame for rendering."""
        pass

    def draw_texture(
        self,
        texture_id: str,
        position: tuple[float, float],
        size: tuple[float, float],
        rotation: float = 0.0,
    ) -> None:
        """Draw a texture on the screen."""
        pass

    def draw_shape(
        self,
        shape_type: str,
        position: tuple[float, float],
        size: tuple[float, float],
        color: tuple[int, int, int],
        rotation: float = 0.0,
    ) -> None:
        """Draw a shape on the screen."""
        pass

    def set_space(self, space: RenderSpace) -> None:
        """Set the current rendering space (e.g., 'world' or 'screen')."""
        pass
