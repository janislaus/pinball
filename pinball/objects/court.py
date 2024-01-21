from pinball.objects.line import Line
from pinball.objects.vector import Vector
from pinball.constants import LEFT_ROTATION_POINT, RIGHT_ROTATION_POINT
import pygame


class Court:
    def __init__(self, screen) -> None:
        self.boundaries = self.get_boundaries(screen=screen)
        self.screen = screen

    def get_boundaries(self, screen) -> list[Line]:
        s = screen
        w = screen.get_width()
        h = screen.get_height()
        return [
            # left
            Line(Vector(0, 0), Vector(0, s.get_height() - 235)),
            # right
            Line(
                Vector(s.get_width(), 150),
                Vector(s.get_width(), s.get_height()),
            ),
            # top
            Line(Vector(0, 0), Vector(s.get_width() - 150, 0)),
            # left rotation to left border
            Line(
                LEFT_ROTATION_POINT,
                LEFT_ROTATION_POINT + Vector(-1, -0.7).normalize() * 300,
            ),
            # right rotation to right border
            Line(
                RIGHT_ROTATION_POINT,
                RIGHT_ROTATION_POINT + Vector(+1, -0.7).normalize() * 150,
            ),
            # left spring boundary
            Line(
                Vector(s.get_width() - 75, s.get_height() - 189),
                Vector(s.get_width() - 75, s.get_height()),
            ),
            # corner above spring
            Line(Vector(s.get_width() - 150, 0), Vector(s.get_width(), 150)),
        ]

    def draw(self):
        for l in self.boundaries:
            pygame.draw.line(
                self.screen,
                (123, 123, 123),
                (l.p1.x, l.p1.y),
                (l.p2.x, l.p2.y),
                width=10,
            )
