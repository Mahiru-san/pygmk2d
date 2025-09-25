from typing import Any, Callable


class EventManager:
    def __init__(self):
        self._events: dict[str, list[Callable[..., Any]]] = {}

    def register(self, event_type: str, function: Callable) -> None:
        self._events.setdefault(event_type, []).append(function)

    def unregister(self, event_type: str, function: Callable) -> None:
        if event_type in self._events.keys():
            self._events[event_type].remove(function)

    def post(self, event_type: str, *args, **kwargs) -> None:
        if event_type not in self._events.keys():
            return
        funcs = self._events[event_type]
        for func in funcs:
            func(*args, **kwargs)
