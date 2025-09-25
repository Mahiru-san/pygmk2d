from dataclasses import dataclass, field
from typing import Any, Iterable, Optional, Protocol


class QuadTreeObject(Protocol):
    def is_intersected_node(self, node: "QuadTreeNode") -> bool: ...


@dataclass
class QuadTreeNode:
    depth: int = 0
    start_point: tuple[float, float] = field(default_factory=tuple)
    end_point: tuple[float, float] = field(default_factory=tuple)
    container: list["int"] = field(default_factory=list)
    reference_list: list[QuadTreeObject] = field(default_factory=list)
    nw_node: Optional["QuadTreeNode"] = None
    ne_node: Optional["QuadTreeNode"] = None
    sw_node: Optional["QuadTreeNode"] = None
    se_node: Optional["QuadTreeNode"] = None

    def get_type(self) -> str:
        return "quadtree"

    def insert(self, index: int) -> None:
        if self.nw_node is None:
            self.container.append(index)
            if len(self.container) > 32 and self.depth < 6:
                self._subdivide()
                for obj in self.container:
                    self._insert_into_subnodes(obj)
                self.container.clear()
        else:
            self._insert_into_subnodes(index)

    def _insert_into_subnodes(self, index: int) -> None:
        if self.nw_node is not None:
            if self._is_in_nw(index):
                self.nw_node.insert(index)
            if self._is_in_ne(index):
                self.ne_node.insert(index)
            if self._is_in_sw(index):
                self.sw_node.insert(index)
            if self._is_in_se(index):
                self.se_node.insert(index)

    def _subdivide(self) -> None:
        mid_x = (self.start_point[0] + self.end_point[0]) / 2
        mid_y = (self.start_point[1] + self.end_point[1]) / 2
        self.nw_node = QuadTreeNode(
            depth=self.depth + 1,
            start_point=self.start_point,
            end_point=(mid_x, mid_y),
            reference_list=self.reference_list,
        )
        self.ne_node = QuadTreeNode(
            depth=self.depth + 1,
            start_point=(mid_x, self.start_point[1]),
            end_point=self.end_point,
            reference_list=self.reference_list,
        )
        self.sw_node = QuadTreeNode(
            depth=self.depth + 1,
            start_point=(self.start_point[0], mid_y),
            end_point=(mid_x, self.end_point[1]),
            reference_list=self.reference_list,
        )
        self.se_node = QuadTreeNode(
            depth=self.depth + 1,
            start_point=(mid_x, mid_y),
            end_point=self.end_point,
            reference_list=self.reference_list,
        )

    def _is_in_nw(self, index: int) -> bool:
        return self.reference_list[index].is_intersected_node(self.nw_node)

    def _is_in_ne(self, index: int) -> bool:
        return self.reference_list[index].is_intersected_node(self.ne_node)

    def _is_in_sw(self, index: int) -> bool:
        return self.reference_list[index].is_intersected_node(self.sw_node)

    def _is_in_se(self, index: int) -> bool:
        return self.reference_list[index].is_intersected_node(self.se_node)

    def interate_tree(self, func: Any) -> None:
        if self.nw_node is not None:
            self.nw_node.interate_tree(func)
            self.ne_node.interate_tree(func)
            self.sw_node.interate_tree(func)
            self.se_node.interate_tree(func)
        else:
            if len(self.container) > 1:
                func(self.container, self.reference_list)

    def iterate_nodes(self) -> Iterable["QuadTreeNode"]:
        yield self
        if self.nw_node is not None:
            yield from self.nw_node.iterate_nodes()
            yield from self.ne_node.iterate_nodes()
            yield from self.sw_node.iterate_nodes()
            yield from self.se_node.iterate_nodes()

    def update(self, resolution: tuple[int, int], time_step: float) -> None:
        pass
