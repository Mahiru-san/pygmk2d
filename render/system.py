from render.context import RenderContext
from render.renderable import RenderableWrapper
from ecs.entity_manager import EntityManager


class RenderSystem:
    def __init__(self, em: EntityManager, render_context: RenderContext) -> None:
        self.render_context = render_context
        self.em = em

    def render(self, alpha: float = 1.0) -> None:
        renderable_ids = self.em.query_entities([RenderableWrapper])
        sorted_renderables: list[RenderableWrapper] = sorted(
            (
                self.em.get_component(eid, RenderableWrapper)
                for eid in renderable_ids
                if self.em.get_component(eid, RenderableWrapper)
            ),
            key=lambda rw: rw.depth,
        )
        for renderable in sorted_renderables:
            if renderable.visible:
                renderable.render(self.render_context, alpha)
        self.render_context.present()
