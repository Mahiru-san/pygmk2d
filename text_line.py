import pygame


class TextLine:
    def __init__(
        self,
        text: str,
        font: pygame.font.Font,
        color: pygame.color.Color,
        position: tuple[int, int] | pygame.Vector2,
    ) -> None:
        self.text = text
        self.font = font
        self.color = color
        self.position = position
        self._rendered_text = self.font.render(self.text, True, self.color)

    def update(self, resolution: tuple[int, int], time_step: float) -> None:
        pass

    def set_position(self, new_position: tuple[int, int] | pygame.Vector2) -> None:
        self.position = new_position

    def get_position(self) -> tuple[int, int] | pygame.Vector2:
        return self.position

    def get_font(self) -> pygame.font.Font:
        return self.font

    def set_font(self, new_font: pygame.font.Font) -> None:
        self.font = new_font
        self._rendered_text = self.font.render(self.text, True, self.color)

    def set_color(self, new_color: pygame.color.Color) -> None:
        self.color = new_color
        self._rendered_text = self.font.render(self.text, True, self.color)

    def get_color(self) -> pygame.color.Color:
        return self.color

    def update_text(self, new_text: str) -> None:
        self.text = new_text
        self._rendered_text = self.font.render(self.text, True, self.color)

    def get_text(self) -> str:
        return self.text

    def get_type(self) -> str:
        return "text_line"


class TextLineRenderer:
    def draw(self, screen: pygame.surface.Surface, obj: TextLine) -> None:
        screen.blit(obj._rendered_text, obj.position)
