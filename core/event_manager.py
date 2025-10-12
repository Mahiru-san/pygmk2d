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
class GameEvent:
    type: EventType
    data: dict[str, Any]


class EventManager:
    def __init__(self, log_policy: LogPolicy = LogPolicy.PRINT) -> None:
        self._events: dict[EventType | str, list[Callable[[GameEvent], Any]]] = {}
        self._event_queue: deque[GameEvent] = deque()
        self.log_policy = log_policy
        self._user_event_prefix = "USER_EVENT_"

    def create_custom_event(self, name: str) -> str:
        return f"{self._user_event_prefix}{name}"

    def register(
        self, event_type: EventType | str, listener: Callable[[GameEvent], Any]
    ) -> None:
        """Subscribe to a specific event type."""
        self._events.setdefault(event_type, []).append(listener)

    def unregister(
        self, event_type: EventType | str, listener: Callable[[GameEvent], Any]
    ) -> None:
        listeners = self._events.get(event_type)
        if listeners and listener in listeners:
            listeners.remove(listener)

    def post(self, event_type: EventType | str, data: dict[str, Any] = None) -> None:
        """Enqueue an event to be processed later."""
        self._event_queue.append(GameEvent(event_type, data or {}))

    def dispatch(self, event: GameEvent) -> None:
        """Immediately process one event."""
        for listener in self._events.get(event.type, []):
            try:
                listener(event)
            except Exception as e:
                if self.log_policy == LogPolicy.PRINT:
                    print(f"Error in event listener: {e}")
                elif self.log_policy == LogPolicy.RAISE:
                    raise

    def process_event_queue(self) -> None:
        """Process all queued events."""
        while self._event_queue:
            event = self._event_queue.popleft()
            self.dispatch(event)
