from typing import Iterable
from .camera import Camera
from .context import RenderContext
from .renderable import (
    UIRenderable,
    WorldRenderable,
    RenderParams,
    RenderSpace,
)
from ..ecs.entity_manager import EntityManager


class RenderSystem:
    def __init__(
        self,
        em: EntityManager,
        context: RenderContext,
        camera: Camera,
        debug: bool = False,
    ) -> None:
        self.em = em
        self.context = context
        self.camera = camera
        self.debug = debug

    def set_context(self, context: RenderContext) -> None:
        self.context = context

    def set_camera(self, camera: Camera) -> None:
        self.camera = camera

    def render(self, alpha: float = 1.0) -> None:
        self.context.start_frame()
        renderable_ids = self.em.query_by_type(WorldRenderable)
        self._render_world(renderable_ids, alpha)
        renderable_ids = self.em.query_by_type(UIRenderable)
        self._render_ui(renderable_ids, alpha)
        self.context.end_frame()

    def _render_world(self, renderable_ids: Iterable[int], alpha: float) -> None:
        self.context.set_space(RenderSpace.WORLD)
        sorted_entity_renderable_pairs: list[tuple[int, WorldRenderable]] = sorted(
            (
                (entity, self.em.get_component(entity, WorldRenderable))
                for entity in renderable_ids
            ),
            key=lambda pair: (pair[1].layer, pair[1].depth),
        )
        for entity, renderable in sorted_entity_renderable_pairs:
            transform = renderable.get_transform(self.em, entity)
            if not transform:
                continue
            if renderable.visible or (renderable.debug_visible and self.debug):
                renderable.render(
                    RenderParams(self.context, alpha, transform, self.camera)
                )

    def _render_ui(self, renderable_ids: Iterable[int], alpha: float) -> None:
        self.context.set_space(RenderSpace.SCREEN)
        renderables: list[UIRenderable] = sorted(
            (self.em.get_component(entity, UIRenderable) for entity in renderable_ids),
            key=lambda r: (r.layer, r.depth),
        )
        for renderable in renderables:
            if renderable.visible:
                renderable.render(RenderParams(self.context, alpha))
