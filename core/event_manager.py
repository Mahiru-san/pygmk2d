from typing import Callable


class EventManager:
    def __init__(self):
        self.events = dict()

    def add_event(self, event_type: str, functions: list[Callable]) -> None:
        self.events[event_type] = functions

    def remove_event(self, event_type: str) -> None:
        self.events.pop(event_type)

    def post_event(self, event_type: str, *args, **kwargs) -> None:
        self._get_func(event_type)(*args, **kwargs)

    def _get_func(self, event_type_input: str) -> Callable:
        for event_type, func in self.events.items():
            if event_type_input == event_type:
                return func
        raise ValueError(f"Event type not exited: {event_type_input}") from None
