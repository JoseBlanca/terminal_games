from enum import Enum

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Label
from textual.reactive import reactive


class XDirection(Enum):
    LEFT = -1
    RIGHT = 1


class YDirection(Enum):
    UP = 1
    DOWN = -1


class GameObject(Label):
    def __init__(self, **kwargs):
        super().__init__()
        self.x = 0
        self.y = 0
        self.bounce_on_edge = True
        self.x_direction = XDirection.RIGHT
        self.y_direction = YDirection.DOWN

    def on_mount(self):
        self.update("*")
        self.styles.position = "absolute"
        self.update_position()

    def update_position(self):
        parent = self.parent
        if parent:
            x_max = parent.container_size.width - 1
            y_max = parent.container_size.height - 1
        else:
            raise RuntimeError("Parent container not found")

        if self.x_direction == XDirection.RIGHT:
            self.x += 1
        else:
            self.x -= 1
        if self.x >= x_max:
            if self.bounce_on_edge:
                self.x_direction = XDirection.LEFT
        elif self.x <= 0:
            if self.bounce_on_edge:
                self.x_direction = XDirection.RIGHT

        if self.y_direction == YDirection.UP:
            self.y -= 1
        else:
            self.y += 1
        if self.y >= y_max:
            if self.bounce_on_edge:
                self.y_direction = YDirection.UP
        elif self.y <= 0:
            if self.bounce_on_edge:
                self.y_direction = YDirection.DOWN

        self.styles.offset = self.x, self.y


class GameApp(App):
    CSS = "Screen { background: black; }"

    def compose(self) -> ComposeResult:
        self.star = GameObject()
        yield Container(self.star)

    def on_mount(self):
        self.set_interval(0.02, self.update_game_objects)

    def update_game_objects(self):
        self.star.update_position()


if __name__ == "__main__":
    GameApp().run()
