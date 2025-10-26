from typing import Any, Callable
from collections import deque
from enum import Enum, auto
from dataclasses import dataclass


class EventType(Enum):
    KEY_DOWN = auto()
    KEY_UP = auto()
    KEY_PRESSED = auto()
    MOUSE_MOVE = auto()
    MOUSE_BUTTON_DOWN = auto()
    MOUSE_BUTTON_UP = auto()
    MOUSE_BUTTON_PRESSED = auto()
    WINDOW_RESIZE = auto()
    QUIT = auto()


class LogPolicy(Enum):
    IGNORE = auto()
    PRINT = auto()
    RAISE = auto()


@dataclass(frozen=True)
class Event:
    type: EventType | str
    data: dict[str, Any]


class EventListenerError(Exception):
    pass


class EventChannel:
    def __init__(self, log_policy: LogPolicy = LogPolicy.PRINT) -> None:
        self._events: dict[EventType | str, list[Callable[[Event], Any]]] = {}
        self._event_queue: deque[Event] = deque()
        self.log_policy = log_policy
        self._user_event_prefix = "USER_EVENT_"

    def create_custom_event(self, name: str) -> str:
        return f"{self._user_event_prefix}{name}"

    def register(
        self, event_type: EventType | str, listener: Callable[[Event], Any]
    ) -> None:
        """Subscribe to a specific event type."""
        self._events.setdefault(event_type, []).append(listener)

    def unregister(
        self, event_type: EventType | str, listener: Callable[[Event], Any]
    ) -> None:
        listeners = self._events.get(event_type)
        if listeners and listener in listeners:
            listeners.remove(listener)

    def post(self, event_type: EventType | str, data: dict[str, Any] = None) -> None:
        """Enqueue an event to be processed later."""
        self._event_queue.append(Event(event_type, data or {}))

    def dispatch(self, event: Event) -> None:
        """Immediately process one event."""
        for listener in self._events.get(event.type, []):
            try:
                listener(event)
            except Exception as e:
                if self.log_policy == LogPolicy.PRINT:
                    print(f"Error in event listener: {listener.__name__}")
                elif self.log_policy == LogPolicy.RAISE:
                    raise EventListenerError(
                        f"Error in event listener: {listener.__name__}"
                    ) from e

    def process_event_queue(self) -> None:
        """Process all queued events."""
        while self._event_queue:
            event = self._event_queue.popleft()
            self.dispatch(event)


class EventManager:
    def __init__(self):
        self._internal_event_channel = EventChannel()
        self._external_event_channel = EventChannel()

    @property
    def internal(self) -> EventChannel:
        return self._internal_event_channel

    @property
    def external(self) -> EventChannel:
        return self._external_event_channel
