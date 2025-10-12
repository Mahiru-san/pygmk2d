from typing import Protocol


class RenderTarget(Protocol):
    """Abstract render target interface for all rendering backends."""

    def present(self) -> None:
        """Present the rendered frame to the display."""
        pass

    def get_size(self) -> tuple[int, int]:
        """Get the size of the render target."""
        pass

    def clear(self, color: tuple[int, int, int]) -> None:
        """Clear the render target with the given color."""
        pass

    def resize(self, size: tuple[int, int]) -> None:
        """Resize the render target to the given size."""
        pass
