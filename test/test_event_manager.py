import pytest
from unittest.mock import MagicMock

from pygmk2d.core.event_manager import (
    EventManager,
    EventChannel,
    Event,
    EventType,
    LogPolicy,
    EventListenerError,
)


# --- Fixtures ---


@pytest.fixture
def event_channel() -> EventChannel:
    """Cung cấp một EventChannel mới cho mỗi bài kiểm thử."""
    return EventChannel()


@pytest.fixture
def event_manager() -> EventManager:
    """Cung cấp một EventManager mới cho mỗi bài kiểm thử."""
    return EventManager()


# --- Kiểm thử Lớp EventChannel ---


def test_channel_register_listener(event_channel: EventChannel):
    """Kiểm tra xem listener có được đăng ký chính xác không."""
    mock_listener = MagicMock()

    event_channel.register(EventType.KEY_DOWN, mock_listener)

    # Kiểm tra cấu trúc dữ liệu nội bộ
    assert EventType.KEY_DOWN in event_channel._events
    assert len(event_channel._events[EventType.KEY_DOWN]) == 1
    assert event_channel._events[EventType.KEY_DOWN][0] == mock_listener


def test_channel_unregister_listener(event_channel: EventChannel):
    """Kiểm tra xem listener có được hủy đăng ký chính xác không."""
    mock_listener = MagicMock()

    # Đăng ký trước
    event_channel.register(EventType.KEY_DOWN, mock_listener)
    assert mock_listener in event_channel._events[EventType.KEY_DOWN]

    # Hủy đăng ký
    event_channel.unregister(EventType.KEY_DOWN, mock_listener)

    assert mock_listener not in event_channel._events[EventType.KEY_DOWN]


def test_channel_unregister_non_existent_listener(event_channel: EventChannel):
    """Kiểm tra việc hủy đăng ký một listener không tồn tại (không nên gây lỗi)."""
    mock_listener = MagicMock()

    try:
        event_channel.unregister(EventType.KEY_DOWN, mock_listener)
        event_channel.unregister("NON_EXISTENT_EVENT", mock_listener)
    except Exception as e:
        pytest.fail(f"Unregistering a non-existent listener raised an exception: {e}")


def test_channel_dispatch_event_immediate(event_channel: EventChannel):
    """Kiểm tra 'dispatch' (xử lý sự kiện ngay lập tức)."""
    mock_listener = MagicMock()
    event_channel.register(EventType.QUIT, mock_listener)

    event_data = {"reason": "user_clicked_x"}
    event_to_dispatch = Event(type=EventType.QUIT, data=event_data)

    event_channel.dispatch(event_to_dispatch)

    # Listener phải được gọi ngay lập tức với đúng đối tượng Event
    mock_listener.assert_called_once_with(event_to_dispatch)


def test_channel_post_and_process_queue(event_channel: EventChannel):
    """Kiểm tra 'post' (thêm vào hàng đợi) và 'process_event_queue' (xử lý hàng đợi)."""
    mock_listener = MagicMock()
    event_channel.register(EventType.KEY_DOWN, mock_listener)

    event_data = {"key": "A", "code": 65}

    # 1. Post sự kiện
    event_channel.post(EventType.KEY_DOWN, event_data)

    # 2. Kiểm tra: Listener CHƯA được gọi, hàng đợi có 1 sự kiện
    mock_listener.assert_not_called()
    assert len(event_channel._event_queue) == 1

    # 3. Xử lý hàng đợi
    event_channel.process_event_queue()

    # 4. Kiểm tra: Listener ĐÃ được gọi, hàng đợi trống
    expected_event = Event(type=EventType.KEY_DOWN, data=event_data)
    mock_listener.assert_called_once_with(expected_event)
    assert len(event_channel._event_queue) == 0


def test_channel_dispatch_no_listeners(event_channel: EventChannel):
    """Kiểm tra việc dispatch một sự kiện không có listener (không nên gây lỗi)."""
    event_to_dispatch = Event(type=EventType.MOUSE_MOVE, data={"x": 100, "y": 100})

    try:
        event_channel.dispatch(event_to_dispatch)
    except Exception as e:
        pytest.fail(f"Dispatching an event with no listeners raised an exception: {e}")


def test_channel_multiple_listeners(event_channel: EventChannel):
    """Kiểm tra nhiều listener cho cùng một sự kiện."""
    listener_a = MagicMock()
    listener_b = MagicMock()

    event_channel.register(EventType.WINDOW_RESIZE, listener_a)
    event_channel.register(EventType.WINDOW_RESIZE, listener_b)

    event_data = {"width": 1024, "height": 768}
    event_to_dispatch = Event(type=EventType.WINDOW_RESIZE, data=event_data)

    event_channel.dispatch(event_to_dispatch)

    # Cả hai listener đều phải được gọi
    listener_a.assert_called_once_with(event_to_dispatch)
    listener_b.assert_called_once_with(event_to_dispatch)


def test_channel_custom_events(event_channel: EventChannel):
    """Kiểm tra việc sử dụng các sự kiện tùy chỉnh (dạng chuỗi)."""
    mock_listener = MagicMock()

    # Tạo tên sự kiện tùy chỉnh
    CUSTOM_EVENT_NAME = event_channel.create_custom_event("PLAYER_JUMP")
    assert CUSTOM_EVENT_NAME == "USER_EVENT_PLAYER_JUMP"

    event_channel.register(CUSTOM_EVENT_NAME, mock_listener)

    event_data = {"power": 100}
    event_to_dispatch = Event(type=CUSTOM_EVENT_NAME, data=event_data)

    event_channel.dispatch(event_to_dispatch)

    mock_listener.assert_called_once_with(event_to_dispatch)


# --- Kiểm thử LogPolicy của EventChannel ---


def test_channel_log_policy_raise(capsys):
    """Kiểm tra LogPolicy.RAISE: Phải ném ra lỗi."""
    # Tạo channel với LogPolicy.RAISE
    channel = EventChannel(log_policy=LogPolicy.RAISE)

    # Tạo listener gây lỗi
    def faulty_listener(event: Event):
        raise ValueError("Test Error")

    channel.register(EventType.KEY_DOWN, faulty_listener)
    event_to_dispatch = Event(type=EventType.KEY_DOWN, data={})

    # Kiểm tra xem lỗi có bị ném ra không
    with pytest.raises(EventListenerError, match="faulty_listener") as exc_info:
        channel.dispatch(event_to_dispatch)
    assert isinstance(exc_info.value.__cause__, ValueError)
    assert str(exc_info.value.__cause__) == "Test Error"


def test_channel_log_policy_print(capsys):
    """Kiểm tra LogPolicy.PRINT (mặc định): Phải in lỗi ra console."""
    # Tạo channel với LogPolicy.PRINT
    channel = EventChannel(log_policy=LogPolicy.PRINT)

    def faulty_listener(event: Event):
        raise ValueError("Test Error")

    channel.register(EventType.KEY_DOWN, faulty_listener)
    event_to_dispatch = Event(type=EventType.KEY_DOWN, data={})

    # Dispatch không nên ném lỗi
    try:
        channel.dispatch(event_to_dispatch)
    except Exception:
        pytest.fail("LogPolicy.PRINT should not raise an exception")

    # Kiểm tra xem lỗi có được in ra không
    captured = capsys.readouterr()
    assert "Error in event listener: faulty_listener" in captured.out


def test_channel_log_policy_ignore(capsys):
    """Kiểm tra LogPolicy.IGNORE: Phải im lặng bỏ qua lỗi."""
    # Tạo channel với LogPolicy.IGNORE
    channel = EventChannel(log_policy=LogPolicy.IGNORE)

    def faulty_listener(event: Event):
        raise ValueError("Test Error")

    channel.register(EventType.KEY_DOWN, faulty_listener)
    event_to_dispatch = Event(type=EventType.KEY_DOWN, data={})

    # Dispatch không nên ném lỗi
    try:
        channel.dispatch(event_to_dispatch)
    except Exception:
        pytest.fail("LogPolicy.IGNORE should not raise an exception")

    # Kiểm tra xem không có gì được in ra
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


# --- Kiểm thử Lớp EventManager ---


def test_event_manager_initialization(event_manager: EventManager):
    """Kiểm tra xem EventManager có khởi tạo 2 channel riêng biệt không."""
    assert event_manager.internal is not None
    assert event_manager.external is not None

    assert isinstance(event_manager.internal, EventChannel)
    assert isinstance(event_manager.external, EventChannel)

    # Quan trọng: chúng phải là 2 đối tượng khác nhau
    assert event_manager.internal is not event_manager.external


def test_event_manager_channels_work_independently(event_manager: EventManager):
    """Kiểm tra internal và external channel hoạt động độc lập."""
    internal_listener = MagicMock()
    external_listener = MagicMock()

    # Đăng ký listener vào các channel tương ứng
    event_manager.internal.register(EventType.KEY_DOWN, internal_listener)
    event_manager.external.register(EventType.KEY_DOWN, external_listener)

    event_data = {"key": "B"}
    event_to_post = Event(type=EventType.KEY_DOWN, data=event_data)

    # Chỉ dispatch trên internal channel
    event_manager.internal.dispatch(event_to_post)

    # Chỉ listener của internal được gọi
    internal_listener.assert_called_once_with(event_to_post)
    external_listener.assert_not_called()
