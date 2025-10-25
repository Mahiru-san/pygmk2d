from ecs.component import Component


class EntityManager:
    def __init__(self):
        self._components: dict[str, dict[int, Component]] = {}
        self._next_entity_id: int = 0

    def create_entity(self) -> int:
        entity_id = self._next_entity_id
        self._next_entity_id += 1
        return entity_id

    def remove_entity(self, entity_id: int) -> None:
        for component_dict in self._components.values():
            if entity_id in component_dict:
                del component_dict[entity_id]

    def add_component(self, entity_id: int, component: Component) -> None:
        component_type = type(component).__name__
        if component_type not in self._components:
            self._components[component_type] = {}
        self._components[component_type][entity_id] = component

    def has_component(self, entity_id: int, component_type: type[Component]) -> bool:
        component_type_name = component_type.__name__
        return (
            component_type_name in self._components
            and entity_id in self._components[component_type_name]
        )

    def remove_component(self, entity_id: int, component_type: type[Component]) -> None:
        component_type_name = component_type.__name__
        if component_type_name in self._components:
            if entity_id in self._components[component_type_name]:
                del self._components[component_type_name][entity_id]

    def get_component(
        self, entity_id: int, component_type: type[Component]
    ) -> Component | None:
        component_type_name = component_type.__name__
        return self._components.get(component_type_name, {}).get(entity_id, None)

    def get_all_components(self, entity_id: int) -> dict[str, Component]:
        result = {}
        for component_type, component_dict in self._components.items():
            if entity_id in component_dict:
                result[component_type] = component_dict[entity_id]
        return result

    def query_by_type(self, component_type: type[Component]) -> tuple[int]:
        if component_type.__name__ not in self._components:
            return ()
        return tuple(self._components[component_type.__name__].keys())

    def filter_entities(self, component_types: list[type[Component]]) -> tuple[int]:
        if not component_types:
            return []

        component_type_names = [ct.__name__ for ct in component_types]
        component_type_names.sort(key=lambda x: len(self._components.get(x, {})))
        common_entities = set(self._components.get(component_type_names[0], {}).keys())
        for component_type_name in component_type_names[1:]:
            common_entities = set(
                entity_id
                for entity_id in common_entities
                if entity_id in self._components.get(component_type_name, {})
            )
        return common_entities
