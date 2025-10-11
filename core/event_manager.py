from typing import Any, Callable


class EventManager:
    def __init__(self):
        self._events: dict[str, list[Callable[..., Any]]] = {}
        self._event_queue: list[tuple[str, tuple[Any, ...], dict[str, Any]]] = []

    def register(self, event_type: str, function: Callable) -> None:
        self._events.setdefault(event_type, []).append(function)

    def unregister(self, event_type: str, function: Callable) -> None:
        if event_type in self._events.keys():
            self._events[event_type].remove(function)

    def dispatch(self, event_type: str, *args, **kwargs) -> None:
        if event_type not in self._events.keys():
            return
        funcs = self._events[event_type]
        for func in funcs:
            func(*args, **kwargs)

    def post(self, event_type: str, *args, **kwargs) -> None:
        self._event_queue.append((event_type, args, kwargs))

    def process_event_queue(self) -> None:
        while self._event_queue:
            event_type, args, kwargs = self._event_queue.pop(0)
            self.dispatch(event_type, *args, **kwargs)
