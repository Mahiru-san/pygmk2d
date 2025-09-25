from typing import Iterable
from core.game_engine import Game
from quadtree import QuadTreeNode
import pygame
import color
import random


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


class QuadTreeRenderer:
    def draw(self, screen: pygame.surface.Surface, obj: QuadTreeNode) -> None:
        for node in obj.iterate_nodes():
            # if len(node.container) == 0:
            #    continue
            self._draw_node(screen, node)

    def _draw_node(self, screen: pygame.surface.Surface, node: QuadTreeNode) -> None:
        pygame.draw.rect(
            screen,
            color.RED,
            (
                pygame.Rect(
                    node.start_point,
                    (
                        node.end_point[0] - node.start_point[0],
                        node.end_point[1] - node.start_point[1],
                    ),
                )
            ),
            1,
        )


class Ball:
    def __init__(
        self,
        radius: int,
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

    def set_radius(self, radius: int) -> None:
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


def is_ball_collided(ball_1: Ball, ball_2: Ball) -> bool:
    dx, dy = ball_1.get_position() - ball_2.get_position()
    total_radius = ball_1.get_radius() + ball_2.get_radius()
    distance_squared = dx * dx + dy * dy
    return distance_squared <= total_radius * total_radius


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
    collision_point = (
        ball_1.get_position() * ball_2.get_radius()
        + ball_2.get_position() * ball_1.get_radius()
    ) / (ball_1.get_radius() + ball_2.get_radius())
    to_calculate_ball, remain_ball = (
        (ball_1, ball_2)
        if ball_1.get_radius() > ball_2.get_radius()
        else (ball_2, ball_1)
    )
    scale_to_radius = (
        to_calculate_ball.get_position().distance_to(collision_point)
        / to_calculate_ball.get_radius()
    )
    position_offset = (1 - scale_to_radius) * (
        to_calculate_ball.get_position() - collision_point
    )
    to_calculate_ball.move(to_calculate_ball.get_position() + position_offset)
    remain_ball.move(remain_ball.get_position() - position_offset)


def strict_collision_update(container: list[int], reference_list: list[Ball]) -> None:
    for i in range(len(container) - 1):
        for j in range(i + 1, len(container)):
            if is_ball_collided(
                reference_list[container[i]], reference_list[container[j]]
            ):
                move_ball_colliding(
                    reference_list[container[i]], reference_list[container[j]]
                )
                exchange_momentum(
                    reference_list[container[i]], reference_list[container[j]], 0.999
                )


class TestGame(Game):
    def __init__(self):
        super().__init__((1280, 720), caption="Test Game")
        self.render_controller.set_background_color(color.BLACK)
        self.render_controller.register_renderer("ball", BallRenderer())
        self.render_controller.register_renderer("quadtree", QuadTreeRenderer())

        self.game_object_manager.add_multi(
            generate_random_balls(500, self.render_controller.get_resolution())
        )
        preset_ball_list = [
            Ball(
                100,
                (50, self.render_controller.get_resolution()[1] / 2),
                color.WHITE,
                10,
                (0, 0),
            ),
        ]
        self.game_object_manager.add_multi(preset_ball_list)
        self.set_fps(240)

    def update(self) -> None:
        self._ball_collision_update()
        super().update()

    def _ball_collision_update(self):
        game_object_list: list[Ball] = self.game_object_manager.get_pool("ball")
        quad_tree = QuadTreeNode(
            depth=0,
            start_point=(0, 0),
            end_point=self.render_controller.get_resolution(),
            reference_list=game_object_list,
        )
        if self.game_object_manager.get_pool("quadtree"):
            self.game_object_manager.remove_pool("quadtree")
        self.game_object_manager.add(quad_tree)
        for i in range(len(game_object_list)):
            quad_tree.insert(i)
        quad_tree.interate_tree(strict_collision_update)

    def run(self) -> None:
        self.running = True
        while self.running:
            self.basic_event_handler()
            self.update()
            self.draw_screen()
            pygame.display.set_caption(
                f"{self._caption} FPS: {int(self._clock.get_fps())}"
            )
        pygame.quit()

    def basic_event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.stop()

    def stop(self) -> None:
        self.running = False


def generate_random_balls(
    quantity: int, resolution: tuple[int, int] | pygame.Vector2
) -> Iterable[Ball]:
    colors = [
        color.RED,
        color.GREEN,
        color.YELLOW,
        color.BLUE,
        color.CYAN,
        color.PURPLE,
    ]
    width, height = int(resolution[0]), int(resolution[1])
    for _ in range(quantity):
        random_size_and_mass = 5  # random.randint(1, 20)
        random_position = (
            random.uniform(0, width) - random_size_and_mass,
            random.uniform(0, height) - random_size_and_mass,
        )
        max_velocity = 1000
        random_velocity = (
            random.uniform(-max_velocity, max_velocity),
            random.uniform(-max_velocity, max_velocity),
        )
        yield Ball(
            random_size_and_mass * 2,
            random_position,
            random.choice(colors),
            random_size_and_mass,
            random_velocity,
        )


def main():
    game = TestGame()
    game.run()


if __name__ == "__main__":
    main()
