from typing import Callable

from render.context import RenderContext


class RenderableWrapper:
    def __init__(
        self,
        render_function: Callable[
            [RenderContext, float],
            None,
        ],
        depth: int = 0,
        visible: bool = True,
    ) -> None:
        self.render_function = render_function
        self.depth = depth
        self.visible = visible

    def render(self, context: RenderContext, alpha: float) -> None:
        self.render_function(context, alpha)
