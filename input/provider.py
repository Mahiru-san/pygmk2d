from typing import Protocol, Iterable
from events import RawInputEvent


class InputProvider(Protocol):
    def poll(self) -> Iterable[RawInputEvent]: ...
