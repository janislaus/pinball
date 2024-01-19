import pygame
from typing import Literal
from pinball.objects.line import Line
from pinball.objects.vector import Vector


class Spring:
    def __init__(self, screen, length_at_rest: int = 60) -> None:
        self.length_at_rest = length_at_rest
        self.rect = pygame.Rect(
            screen.get_width() - 60, screen.get_height() - 85, 35, length_at_rest
        )
        self.state: Literal["compressing", "releasing", "resting"] = "resting"
        self.v = 0
        self.screen = screen

    @property
    def boundaries(self) -> list[Line]:
        r = self.rect
        return [
            Line(Vector(r.left, r.top), Vector(r.right, r.top)),
            Line(Vector(r.left, r.bottom), Vector(r.right, r.bottom)),
            Line(Vector(r.right, r.top), Vector(r.right, r.bottom)),
            Line(Vector(r.left, r.top), Vector(r.left, r.bottom)),
        ]

    def draw(self):
        pygame.draw.rect(
            surface=self.screen, color=(250, 30, 0), rect=self.rect, width=25
        )

    def compress(self):
        if self.rect.height > 10:
            self.rect.move_ip(0, +1)
            self.rect.height -= 1

    def release(self):
        """
        Updates position of rectangle
        """

        counter = 0

        if self.rect.height <= self.length_at_rest:
            self.v += 2
            self.rect.height += self.v
            self.rect.y -= self.v
        else:
            self.v = 0
            self.state = "resting"

        # based on previous state calculate next

        # update position of rectangle, yield
        # stop updating when spring fully released --> self.releasing = False,
        # assign new position to rectangle
        # check if rectangle position exceeds max
        # if not --> yield
        # else: self.releasing = False
        # pass

    def update(self):
        if self.state == "compressing":
            self.compress()
        elif self.state == "releasing":
            self.release()
