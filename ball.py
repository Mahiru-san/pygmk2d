import random
import pygame
from quadtree import QuadTreeNode


class Ball:
    def __init__(
        self,
        radius: float,
        position: tuple[float, float] | pygame.Vector2,
        color: pygame.color.Color,
        mass: float,
        velocity: tuple[float, float] | pygame.Vector2 = (0.0, 0.0),
    ) -> None:
        self._radius = radius
        self._position = pygame.Vector2(position)
        self._color = color
        self._mass = mass
        self.set_velocity(velocity)

    def __str__(self) -> str:
        return (
            f"Radius: {self._radius}, "
            f"Center: {self._position}, "
            f"Color: {self._color}, "
            f"Mass: {self._mass}"
            f"Velocity: {self._velocity}"
        )

    def get_type(self) -> str:
        return "ball"

    def move(self, position: tuple[float, float] | pygame.math.Vector2) -> None:
        self._position = pygame.Vector2(position)

    def get_position(self) -> pygame.Vector2:
        return self._position

    def set_radius(self, radius: float) -> None:
        self._radius = radius

    def get_radius(self):
        return self._radius

    def set_color(self, color: pygame.color.Color) -> None:
        self._color = color

    def get_color(self) -> pygame.color.Color:
        return self._color

    def set_mass(self, mass: float) -> None:
        self._mass = mass

    def get_mass(self) -> float:
        return self._mass

    def set_velocity(self, velocity: tuple[float, float] | pygame.Vector2) -> None:
        self._velocity = pygame.Vector2(velocity)

    def get_velocity(self) -> pygame.Vector2:
        return self._velocity

    def update(self, resolution: tuple[int, int], time_step: float) -> None:
        if self.is_vertical_screen_border_collided(resolution[0]):
            self._velocity.x = -self._velocity.x
            self.move(
                (
                    (
                        self._radius
                        if self._position.x < self._radius
                        else resolution[0] - self._radius
                    ),
                    self._position.y,
                )
            )
        if self.is_horizontal_screen_border_collided(resolution[1]):
            self._velocity.y = -self._velocity.y
            self.move(
                (
                    self._position.x,
                    (
                        self._radius
                        if self._position.y < self._radius
                        else resolution[1] - self._radius
                    ),
                )
            )
        x_offset = self._velocity.x * time_step
        y_offset = self._velocity.y * time_step
        new_position = self.get_position() + pygame.Vector2(x_offset, y_offset)
        self.move(new_position)

    def is_horizontal_screen_border_collided(self, height: int) -> bool:
        return not (
            self.get_radius() - 1
            < self.get_position().y
            < height - self.get_radius() + 1
        )

    def is_vertical_screen_border_collided(self, width: int) -> bool:
        return not (
            self.get_radius() - 1
            < self.get_position().x
            < width - self.get_radius() + 1
        )

    def is_intersected_node(self, node: QuadTreeNode) -> bool:
        return circle_intersects_rect(
            self.get_position().x,
            self.get_position().y,
            self.get_radius(),
            node.start_point[0],
            node.start_point[1],
            node.end_point[0],
            node.end_point[1],
        )


class BallRenderer:
    def draw(self, screen: pygame.surface.Surface, obj: Ball) -> None:
        pygame.draw.circle(
            screen,
            obj.get_color(),
            (int(obj.get_position().x), int(obj.get_position().y)),
            obj.get_radius(),
        )


def circle_intersects_rect(cx, cy, radius, rx_min, ry_min, rx_max, ry_max) -> bool:
    """
    Check if a circle intersects an axis-aligned rectangle.

    cx, cy     : center of the circle
    radius     : radius of the circle
    rx_min, ry_min : rectangle min corner (bottom-left)
    rx_max, ry_max : rectangle max corner (top-right)
    """
    # Step 1: Clamp circle center to rectangle
    closest_x = max(rx_min, min(cx, rx_max))
    closest_y = max(ry_min, min(cy, ry_max))

    # Step 2: Compute squared distance to closest point
    dx = closest_x - cx
    dy = closest_y - cy
    dist_sq = dx * dx + dy * dy

    # Step 3: Check if distance is less than or equal to radius
    return dist_sq <= radius * radius


def is_ball_collided(ball_1: Ball, ball_2: Ball) -> bool:
    dx, dy = ball_1.get_position() - ball_2.get_position()
    total_radius = ball_1.get_radius() + ball_2.get_radius()
    distance_squared = dx * dx + dy * dy
    return distance_squared - total_radius * total_radius <= -1e-6


def exchange_momentum(ball_1: Ball, ball_2: Ball, coe: float) -> None:
    vel_1 = ball_1.get_velocity()
    vel_2 = ball_2.get_velocity()
    mass_1 = ball_1.get_mass()
    mass_2 = ball_2.get_mass()
    pos_1 = ball_1.get_position()
    pos_2 = ball_2.get_position()
    normal_unit_vector = (pos_1 - pos_2) / pos_1.distance_to(pos_2)
    coefficent = (1 + coe) / (mass_1 + mass_2)
    new_vel_1 = (
        vel_1
        - coefficent
        * mass_2
        * (vel_1 - vel_2).dot(normal_unit_vector)
        * normal_unit_vector
    )
    new_vel_2 = (
        vel_2
        + coefficent
        * mass_1
        * (vel_1 - vel_2).dot(normal_unit_vector)
        * normal_unit_vector
    )
    ball_1.set_velocity(new_vel_1)
    ball_2.set_velocity(new_vel_2)


def move_ball_colliding(ball_1: Ball, ball_2: Ball):
    if ball_1.get_position() == ball_2.get_position():
        ball_1.move(ball_1.get_position() + (random.random(), random.random()))
    delta_vector = ball_1.get_position() - ball_2.get_position()
    center_distance = delta_vector.magnitude()
    normal_vector = delta_vector / center_distance
    offset_vector = (
        ball_1.get_radius() + ball_2.get_radius() - center_distance
    ) * normal_vector
    total_mass = ball_1.get_mass() + ball_2.get_mass()
    new_position_1 = (
        ball_1.get_position() + ball_2.get_mass() / total_mass * offset_vector
    )
    new_position_2 = (
        ball_2.get_position() - ball_1.get_mass() / total_mass * offset_vector
    )
    ball_1.move(new_position_1)
    ball_2.move(new_position_2)
