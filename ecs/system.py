from ecs.entity_manager import EntityManager


class System:
    def __init__(self, ecs: EntityManager):
        self._ecs = ecs

    def update(self, delta_time: float) -> None:
        raise NotImplementedError("Update method must be implemented by subclasses")
