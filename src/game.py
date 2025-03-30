from enum import Enum

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Label
from textual.reactive import reactive

BALL_X_SPEED = 1
BALL_Y_SPEED = 1


class XDirection(Enum):
    LEFT = -1
    RIGHT = 1


class YDirection(Enum):
    UP = 1
    DOWN = -1


class GameObject:
    def __init__(self, playground: Container):
        self.playground = playground
        self.x = 0
        self.y = 0
        self.bounce_on_edge = True
        self.x_direction = XDirection.RIGHT
        self.y_direction = YDirection.DOWN
        self.ball = Label("*")
        self.textual_widgets = [self.ball]

    def update_position(self):
        x_max = self.playground.container_size.width - 1
        y_max = self.playground.container_size.height - 1

        if self.x_direction == XDirection.RIGHT:
            self.x += BALL_X_SPEED
        else:
            self.x -= BALL_X_SPEED
        if self.x >= x_max:
            if self.bounce_on_edge:
                self.x_direction = XDirection.LEFT
        elif self.x <= 0:
            if self.bounce_on_edge:
                self.x_direction = XDirection.RIGHT

        if self.y_direction == YDirection.UP:
            self.y -= BALL_Y_SPEED
        else:
            self.y += BALL_Y_SPEED
        if self.y >= y_max:
            if self.bounce_on_edge:
                self.y_direction = YDirection.UP
        elif self.y <= 0:
            if self.bounce_on_edge:
                self.y_direction = YDirection.DOWN

        self.ball.styles.offset = round(self.x), round(self.y)


class Playground(Container):
    pass


class GameApp(App):
    CSS = "Screen { background: black; }"

    def __init__(self):
        super().__init__()

        self.playground = Playground()

        ball = GameObject(playground=self.playground)
        self.game_objects = [ball]

    def compose(self) -> ComposeResult:
        yield self.playground

    def on_mount(self):
        self.set_interval(0.02, self.update_game_objects)
        widgets = [
            widget for obj in self.game_objects for widget in obj.textual_widgets
        ]
        self.playground.mount(*widgets)

    def update_game_objects(self):
        for obj in self.game_objects:
            obj.update_position()


if __name__ == "__main__":
    GameApp().run()
