from typing import Protocol
from target import RenderTarget


class RenderContext(Protocol):
    """Abstract renderer interface for all rendering backends."""

    def get_target(self) -> RenderTarget:
        """Get the current render target."""
        pass

    def set_target(self, target: RenderTarget) -> None:
        """Set the current render target."""
        pass

    def clear(self, color: tuple[int, int, int]) -> None:
        """Clear the screen with the specified color."""
        pass

    def draw_line(
        self,
        start_pos: tuple[int, int],
        end_pos: tuple[int, int],
        color: tuple[int, int, int],
        width: int = 1,
    ) -> None:
        """Draw a line on the screen."""
        pass

    def draw_circle(
        self,
        center: tuple[int, int],
        radius: int,
        color: tuple[int, int, int],
        width: int = 0,
    ) -> None:
        """Draw a circle on the screen."""
        pass

    def draw_solid_circle(
        self, center: tuple[int, int], radius: int, color: tuple[int, int, int]
    ) -> None:
        """Draw a solid circle on the screen."""
        pass

    def draw_rect(
        self,
        rect: tuple[int, int, int, int],
        color: tuple[int, int, int],
        width: int = 0,
    ) -> None:
        """Draw a rectangle on the screen."""
        pass

    def draw_solid_rect(
        self, rect: tuple[int, int, int, int], color: tuple[int, int, int]
    ) -> None:
        """Draw a solid rectangle on the screen."""
        pass

    def draw_text(
        self,
        text: str,
        font: str,
        position: tuple[int, int],
        color: tuple[int, int, int],
    ) -> None:
        """Draw text on the screen."""
        pass

    def draw_image(
        self,
        image_path: str,
        position: tuple[int, int],
        size: tuple[int, int] | None = None,
    ) -> None:
        """Draw an image on the screen."""
        pass

    def get_resolution(self) -> tuple[int, int]:
        """Get the current screen resolution."""
        pass

    def set_resolution(self, resolution: tuple[int, int]) -> None:
        """Set the screen resolution."""
        pass

    def present(self) -> None:
        """Present the rendered frame to the display."""
        pass
