from functools import partial
import pygame
from typing import Literal
from pinball.objects.line import Line
from pinball.objects.vector import Vector


def return_spring_v(collision_point, v):
    return v


class Spring:
    def __init__(self, screen, length_at_rest: int = 80) -> None:
        self.length_at_rest = length_at_rest
        self.rect = pygame.Rect(
            screen.get_width() - 67,
            screen.get_height() - length_at_rest,
            60,
            length_at_rest,
        )
        self.state: Literal["compressing", "releasing", "resting"] = "resting"
        self.v = Vector(0, 0)
        self.screen = screen

    @property
    def boundaries(self) -> list[Line]:
        r = self.rect
        return [
            Line(
                Vector(r.left, r.top),
                Vector(r.right, r.top),
                partial(return_spring_v, v=-2.5 * self.v),
            ),
            Line(Vector(r.left, r.bottom), Vector(r.right, r.bottom)),
            Line(Vector(r.right, r.top), Vector(r.right, r.bottom)),
            Line(Vector(r.left, r.top), Vector(r.left, r.bottom)),
        ]

    def draw(self):
        pygame.draw.rect(
            surface=self.screen, color=(250, 30, 0), rect=self.rect, width=0
        )

    def compress(self):
        if self.rect.height > 10:
            self.rect.move_ip(0, +1)
            self.rect.height -= 1

    def release(self):
        """
        Updates position of rectangle
        """

        if self.rect.height <= self.length_at_rest:
            self.v.y += 1
            self.rect.height += int(self.v.y)
            self.rect.y -= int(self.v.y)
        else:
            self.v.y = 0
            self.state = "resting"

    def update(self):
        if self.state == "compressing":
            self.compress()
        elif self.state == "releasing":
            self.release()
