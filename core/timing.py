from abc import ABC, abstractmethod


class Clock(ABC):
    @abstractmethod
    def delta(self) -> float:
        """Get the time elapsed since the last call in seconds."""
        pass

    @abstractmethod
    def now(self) -> float:
        """Get the current time in seconds."""
        pass

    @abstractmethod
    def sleep(self, seconds: float) -> None:
        """Sleep for the specified number of seconds."""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Reset the clock's internal timer."""
        pass
