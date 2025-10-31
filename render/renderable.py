from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Optional
import weakref

from ..ecs.component import Component
from ..ecs.entity_manager import EntityManager
from .camera import Camera
from .context import RenderContext, RenderSpace
from .transform import Transform


@dataclass(frozen=True)
class RenderParams:
    context: RenderContext
    alpha: float
    transform: Optional[Transform] = None
    camera: Optional[Camera] = None


class RenderableBase(Component):
    def __init__(
        self,
        render_function: Callable[
            [RenderParams],
            None,
        ],
        space: RenderSpace,
        layer: int = 0,
        depth: int = 0,
        visible: bool = True,
    ) -> None:
        self.render_function = render_function
        self.layer = layer
        self.depth = depth
        self.space = space
        self.visible = visible

    def render(self, params: RenderParams) -> None:
        self.render_function(params)


class UIRenderable(RenderableBase):

    def __init__(
        self,
        render_function: Callable[
            [RenderParams],
            None,
        ],
        layer: int = 0,
        depth: int = 0,
        visible: bool = True,
    ) -> None:
        super().__init__(
            render_function,
            RenderSpace.SCREEN,
            layer,
            depth,
            visible,
        )


class WorldRenderable(RenderableBase):

    def __init__(
        self,
        render_function: Callable[
            [RenderParams],
            None,
        ],
        transform: Transform | None = None,
        layer: int = 0,
        depth: int = 0,
        visible: bool = True,
        debug_visible: bool = False,
    ) -> None:
        super().__init__(
            render_function,
            RenderSpace.WORLD,
            layer,
            depth,
            visible,
        )
        self.transform_ref = weakref.ref(transform) if transform else None
        self.debug_visible = debug_visible

    def get_transform(self, em: EntityManager, entity: int) -> Transform | None:
        transform = em.get_component(entity, Transform)
        if transform:
            return transform
        return self.transform_ref
