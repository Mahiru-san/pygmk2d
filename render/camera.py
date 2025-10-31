from .transform import Transform


class Camera:
    def __init__(
        self, viewport: tuple[int, int], position: tuple[float, float], zoom: float
    ) -> None:
        self.viewport = viewport
        self.position = position
        self.zoom = zoom

    def set_viewport(self, viewport: tuple[int, int]):
        self.viewport = viewport

    def move(self, delta: tuple[float, float]) -> None:
        self.position = (self.position[0] + delta[0], self.position[1] + delta[1])

    def set_zoom(self, zoom: float) -> None:
        self.zoom = zoom

    def world_to_screen(self, world_pos: tuple[float, float]) -> tuple[float, float]:
        screen_x = (world_pos[0] - self.position[0]) * self.zoom
        screen_y = (world_pos[1] - self.position[1]) * self.zoom
        return (screen_x, screen_y)

    def size_to_screen(self, world_size: tuple[float, float]) -> tuple[float, float]:
        screen_width = world_size[0] * self.zoom
        screen_height = world_size[1] * self.zoom
        return (screen_width, screen_height)

    def transform_rect(
        self, world_pos: tuple[float, float], world_size: tuple[float, float]
    ) -> tuple[float, float, float, float]:
        screen_pos = self.world_to_screen(world_pos)
        screen_size = self.size_to_screen(world_size)
        return (screen_pos, screen_size)

    def is_visible(self, transform: Transform, bounds: tuple[float, float]) -> bool:
        screen_pos = self.world_to_screen(transform.position)
        return (
            screen_pos[0] + bounds[0] > 0
            and screen_pos[1] + bounds[1] > 0
            and screen_pos[0] - bounds[0] < self.viewport[0]
            and screen_pos[1] - bounds[0] < self.viewport[1]
        )
