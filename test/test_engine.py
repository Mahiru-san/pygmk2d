import pytest
from unittest.mock import MagicMock
import math


from pygmk2d.core.engine import Engine


# fixture
@pytest.fixture
def engine() -> Engine:
    """Cung cấp một Engine mới cho mỗi bài kiểm thử."""
    em = MagicMock()
    render_context = MagicMock()
    event_manager = MagicMock()
    input_provider = MagicMock()
    clock = MagicMock()
    camera = MagicMock()

    return Engine(
        em=em,
        render_context=render_context,
        event_manager=event_manager,
        input_provider=input_provider,
        clock=clock,
        camera=camera,
    )


def test_engine_initialization():
    em = MagicMock()
    render_context = MagicMock()
    event_manager = MagicMock()
    input_provider = MagicMock()
    clock = MagicMock()
    camera = MagicMock()

    engine = Engine(
        em=em,
        render_context=render_context,
        event_manager=event_manager,
        input_provider=input_provider,
        clock=clock,
        camera=camera,
    )

    assert engine.em == em
    assert engine.render_system is not None
    assert engine.event_manager == event_manager
    assert engine.input_manager is not None
    assert engine.clock == clock
    assert engine.fixed_dt == 1 / 60
    assert engine.min_frame_time == 1 / 60
    assert engine.running is False


def test_set_max_fps(engine: Engine):
    engine.set_max_fps(240)
    assert math.isclose(engine.min_frame_time, 1 / 240)


def test_set_max_fps_zero(engine: Engine):
    engine.set_max_fps(0)
    assert engine.min_frame_time == float("inf")


def test_add_systems(engine: Engine):

    class DummySystem:
        def __init__(self, em):
            pass

    engine.add_fixed_delta_system(DummySystem)
    engine.add_variable_delta_system(DummySystem)

    assert isinstance(engine._fixed_delta_systems[0], DummySystem)
    assert isinstance(engine._variable_delta_systems[0], DummySystem)


def test_frame_time_under_limit(engine: Engine):
    engine.set_max_fps(60)
    engine.clock.now = MagicMock(side_effect=[0.01])  # Simulate time passage
    engine.clock.sleep = MagicMock()
    engine.enforce_fps_limit(0.0)
    engine.clock.sleep.assert_called_once_with(seconds=engine.min_frame_time - 0.01)


def test_frame_time_over_limit(engine: Engine):
    engine.set_max_fps(60)
    engine.clock.now = MagicMock(side_effect=[0.02])  # Simulate time passage
    engine.clock.sleep = MagicMock()
    engine.enforce_fps_limit(0.0)
    engine.clock.sleep.assert_not_called()


def test_stop_commands_running(engine: Engine):
    engine.running = True
    engine.stop()
    assert not engine.running


def test_step_calls_systems(engine: Engine):
    engine.set_fixed_dt(0.01)
    engine.input_manager.poll = MagicMock()
    engine.event_manager.external.process_event_queue = MagicMock()
    engine.event_manager.internal.process_event_queue = MagicMock()
    engine.render_system.render = MagicMock()

    class DummySystem:
        def __init__(self, em):
            self.update = MagicMock()

    engine.add_fixed_delta_system(DummySystem)
    engine.add_variable_delta_system(DummySystem)
    engine.step(0.016)
    engine.input_manager.poll.assert_called_once()
    engine.event_manager.external.process_event_queue.assert_called_once()
    engine.event_manager.internal.process_event_queue.assert_called_once()
    engine.render_system.render.assert_called_once()
    engine._fixed_delta_systems[0].update.assert_called_once_with(0.01)
    engine._variable_delta_systems[0].update.assert_called_once_with(0.016)
