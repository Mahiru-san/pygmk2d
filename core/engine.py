from core.event_manager import EventManager
from input.provider import InputProvider
from render.context import RenderContext
from ecs.entity_manager import EntityManager
from ecs.system import System
from render.system import RenderSystem
from input.manager import InputManager
from core.timing import Clock


class Engine:
    def __init__(
        self,
        em: EntityManager,
        render_context: RenderContext,
        event_manager: EventManager,
        input_provider: InputProvider,
        clock: Clock,
        fixed_dt: float = 1 / 60,
    ) -> None:
        self.em = em
        self.render_system = RenderSystem(em, render_context)
        self.event_manager = event_manager
        self.input_manager = InputManager(event_manager, input_provider)
        self.clock = clock
        self.fixed_dt = fixed_dt
        self._fixed_delta_systems: list[System] = []
        self._variable_delta_systems: list[System] = []
        self.min_frame_time = 1 / 60  # Default to 60 FPS
        self.running = False

    def set_max_fps(self, fps: int) -> None:
        self.min_frame_time = 1 / fps

    def set_fixed_dt(self, fixed_dt: float) -> None:
        self.fixed_dt = fixed_dt

    def add_fixed_delta_system(self, system: type[System]) -> None:
        self._fixed_delta_systems.append(system(self.em))

    def add_variable_delta_system(self, system: type[System]) -> None:
        self._variable_delta_systems.append(system(self.em))

    def enforce_fps_limit(self, start_time: float) -> None:
        frame_time = self.clock.now() - start_time
        if frame_time < self.min_frame_time:
            sleep_time = self.min_frame_time - frame_time
            self.clock.sleep(seconds=sleep_time)

    def run(self) -> None:
        self.running = True
        self.accumulator = 0.0
        self.clock.reset()
        while self.running:
            start_time = self.clock.now()
            dt = self.clock.delta()
            self.step(dt)
            self.enforce_fps_limit(start_time)

    def step(self, dt: float) -> None:
        self.accumulator += dt
        self.input_manager.poll()
        self.event_manager.external.process_event_queue()

        while self.accumulator >= self.fixed_dt:
            for sys in self._fixed_delta_systems:
                sys.update(self.fixed_dt)
            self.accumulator -= self.fixed_dt

        for sys in self._variable_delta_systems:
            sys.update(dt)

        self.event_manager.internal.process_event_queue()

        alpha = self.accumulator / self.fixed_dt
        self.render_system.render(alpha)

    def stop(self) -> None:
        self.running = False
