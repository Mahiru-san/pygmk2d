from events import RawInputEvent, RawInputType
from provider import InputProvider
from core.event_manager import EventManager, EventType


class InputManager:
    def __init__(self, event_manager: EventManager, provider: InputProvider) -> None:
        self.event_manager = event_manager
        self.provider = provider
        self._pressed_keys: set[int] = set()
        self._pressed_buttons: set[int] = set()
        self._mouse_position: tuple[int, int] = (0, 0)
        self._window_size: tuple[int, int] = (800, 600)  # Default size

    def poll(self) -> None:
        for raw_event in self.provider.poll():
            self._handle_raw_event(raw_event)
            self._update_pressed_states(raw_event)

    def _handle_raw_event(self, raw_event: RawInputEvent) -> None:
        if raw_event.type == RawInputType.KEY_DOWN:
            key = raw_event.data.get("key")
            if key is not None:
                self.event_manager.post(EventType.KEY_DOWN, {"key": key})
                if key not in self._pressed_keys:
                    self.event_manager.post(EventType.KEY_PRESSED, {"key": key})
        elif raw_event.type == RawInputType.KEY_UP:
            key = raw_event.data.get("key")
            if key is not None:
                self.event_manager.post(EventType.KEY_UP, {"key": key})
        elif raw_event.type == RawInputType.MOUSE_MOVE:
            pos = raw_event.data.get("position")
            if pos is not None:
                self._mouse_position = pos
                self.event_manager.post(EventType.MOUSE_MOVE, {"position": pos})
        elif raw_event.type == RawInputType.MOUSE_BUTTON_DOWN:
            button = raw_event.data.get("button")
            if button is not None:
                self.event_manager.post(EventType.MOUSE_BUTTON_DOWN, {"button": button})
                if button not in self._pressed_buttons:
                    self.event_manager.post(
                        EventType.MOUSE_BUTTON_PRESSED, {"button": button}
                    )
        elif raw_event.type == RawInputType.MOUSE_BUTTON_UP:
            button = raw_event.data.get("button")
            if button is not None:
                self.event_manager.post(EventType.MOUSE_BUTTON_UP, {"button": button})
        elif raw_event.type == RawInputType.RESIZE:
            size = raw_event.data.get("size")
            if size is not None:
                self._window_size = size
                self.event_manager.post(EventType.WINDOW_RESIZE, {"size": size})
        elif raw_event.type == RawInputType.QUIT:
            self.event_manager.post(EventType.QUIT, {})

    def _update_pressed_states(self, raw_event: RawInputEvent) -> None:
        if raw_event.type == RawInputType.KEY_DOWN:
            key = raw_event.data.get("key")
            if key is not None:
                self._pressed_keys.add(key)
        elif raw_event.type == RawInputType.KEY_UP:
            key = raw_event.data.get("key")
            if key is not None and key in self._pressed_keys:
                self._pressed_keys.remove(key)
        elif raw_event.type == RawInputType.MOUSE_BUTTON_DOWN:
            button = raw_event.data.get("button")
            if button is not None:
                self._pressed_buttons.add(button)
        elif raw_event.type == RawInputType.MOUSE_BUTTON_UP:
            button = raw_event.data.get("button")
            if button is not None and button in self._pressed_buttons:
                self._pressed_buttons.remove(button)

    def is_key_pressed(self, key: int) -> bool:
        return key in self._pressed_keys

    def is_button_pressed(self, button: int) -> bool:
        return button in self._pressed_buttons

    def get_mouse_position(self) -> tuple[int, int]:
        return self._mouse_position

    def get_window_size(self) -> tuple[int, int]:
        return self._window_size
