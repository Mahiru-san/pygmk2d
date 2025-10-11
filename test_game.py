from typing import Iterable
from core.game_engine import Game
from quadtree import QuadTreeNode
from ball import Ball, is_ball_collided, move_ball_colliding, exchange_momentum
import pygame
import color
import random


class QuadTreeRenderer:
    def draw(self, screen: pygame.surface.Surface, obj: QuadTreeNode) -> None:
        for node in obj.iterate_nodes():
            # if len(node.container) == 0:
            #    continue
            # if node.depth != 3:
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


class BallRenderer:
    def draw(self, screen: pygame.surface.Surface, obj: Ball) -> None:
        pygame.draw.circle(
            screen,
            obj.get_color(),
            (int(obj.get_position().x), int(obj.get_position().y)),
            obj.get_radius(),
        )


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
                    reference_list[container[i]], reference_list[container[j]], 0.001
                )


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
        random_size_and_mass = 1  # random.randint(1, 20)
        random_position = (
            random.uniform(random_size_and_mass, width - random_size_and_mass),
            random.uniform(random_size_and_mass, height - random_size_and_mass),
        )
        max_velocity = 200
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


class TestGame(Game):
    def __init__(self):
        super().__init__((1280, 720), caption="Test Game")
        self.render_controller.set_background_color(color.BLACK)
        self.render_controller.register_renderer("ball", BallRenderer())
        self.render_controller.register_renderer("quadtree", QuadTreeRenderer())

        self.game_object_manager.add_multi(
            generate_random_balls(1000, self.render_controller.get_resolution())
        )
        """preset_ball_list = [
            Ball(
                100,
                (50, self.render_controller.get_resolution()[1] / 2),
                color.WHITE,
                10,
                (0, 0),
            ),
            Ball(
                100,
                (40, self.render_controller.get_resolution()[1] / 2),
                color.WHITE,
                20,
                (100, 0),
            ),
        ]"""
        """preset_ball_list = []
        for i in range(0, 50):
            preset_ball_list.append(
                Ball(
                    1,
                    ((10 + 20 * i), self.render_controller.get_resolution()[1] / 2),
                    color.WHITE,
                    1,
                    (500 + 20 * i, 0),
                )
            )"""
        # self.game_object_manager.add_multi(preset_ball_list)
        self.set_fps(240)
        self.spawn_time_marker = 0
        self.spawn_ball_size = 2

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
                if event.key == pygame.K_r:
                    self.game_object_manager.remove_pool("ball")
                if event.key == pygame.K_UP:
                    self.spawn_ball_size += 1
                    if self.spawn_ball_size > 20:
                        self.spawn_ball_size = 20
                if event.key == pygame.K_DOWN:
                    self.spawn_ball_size -= 1
                    if self.spawn_ball_size < 1:
                        self.spawn_ball_size = 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.spawn_time_marker = pygame.time.get_ticks()
                    self.game_object_manager.add(
                        Ball(
                            self.spawn_ball_size,
                            event.pos,
                            color.WHITE,
                            self.spawn_ball_size * 2 * 3.14,
                            (random.uniform(-100, 100), random.uniform(-100, 100)),
                        )
                    )
        if pygame.mouse.get_pressed(3)[0]:
            if self.spawn_time_marker + 50 > pygame.time.get_ticks():
                return
            self.spawn_time_marker = pygame.time.get_ticks()
            mouse_position = pygame.mouse.get_pos()
            self.game_object_manager.add(
                Ball(
                    self.spawn_ball_size,
                    mouse_position,
                    color.WHITE,
                    self.spawn_ball_size * 2 * 3.14,
                    (random.uniform(-100, 100), random.uniform(-100, 100)),
                )
            )

    def stop(self) -> None:
        self.running = False


def main():
    game = TestGame()
    game.run()


if __name__ == "__main__":
    main()
