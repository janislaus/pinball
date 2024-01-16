from pinball.objects.line import Line
from pinball.objects.point import Point
import pygame


class Court:
    def __init__(self, screen) -> None:
        self.boundaries = self.get_boundaries(screen=screen)
        self.screen = screen

    def get_boundaries(self, screen) -> list[Line]:
        s = screen
        shift = 0
        return [
            Line(Point(shift, shift), Point(shift, s.get_height() - shift)),
            Line(
                Point(s.get_width() - shift, shift),
                Point(s.get_width() - shift, s.get_height() - shift),
            ),
            Line(Point(0, 0), Point(s.get_width(), 0)),
            Line(
                Point(s.get_width() - shift, s.get_height() - shift),
                Point(0 + shift, s.get_height() - shift),
            ),
        ]

    def draw(self):
        for l in self.boundaries:
            pygame.draw.line(
                self.screen, (255, 255, 255), (l.p1.x, l.p1.y), (l.p2.x, l.p2.y)
            )
