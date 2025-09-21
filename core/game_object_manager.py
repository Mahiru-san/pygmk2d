from typing import Any, Generator, Iterable
from requirements import GameObject


class GameObjectManager:
    def __init__(self):
        """Generates a new GameObjectManager"""
        self.empty()

    def add(self, game_object: GameObject) -> None:
        """Add a new GameObject to GameObject list

        Args:
            game_object (GameObject): A game object
        """
        self._game_objects.setdefault(game_object.get_type(), []).append(game_object)

    def add_multi(self, game_objects: Iterable[GameObject]) -> None:
        """Add multiple GameObject to GameObject list

        Args:
            game_objects (list[GameObject]): A list containing multiple GameObject
        """
        for game_object in game_objects:
            self.add(game_object)

    def remove_pool(self, pool_type: str = "unknown") -> None:
        """remove a GameObject pool

        Args:
            pool_type (str): Pool type to be removed
        """
        self._game_objects[pool_type].clear()

    def get_all(self) -> Generator[GameObject, None, None]:
        """get all GameObject"""
        for key in self._game_objects.keys():
            for obj in self._game_objects.get(key, []):
                yield obj

    def get_pool(self, pool_type: str) -> list[Any]:
        """get pool of specific type"""
        return self._game_objects.get(pool_type, [])

    def empty(self) -> None:
        """empty all GameObject pools"""
        self._game_objects: dict[str, list[GameObject]] = {}

    def is_empty(self) -> bool:
        """is GameObject empty"""
        return (
            sum(
                [
                    len(self._game_objects.get(key, []))
                    for key in self._game_objects.keys()
                ]
            )
            == 0
        )
