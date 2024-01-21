from pinball.objects.line import Line
from pinball.objects.vector import Vector
import pygame


class Court:
    def __init__(self, screen) -> None:
        self.boundaries = self.get_boundaries(screen=screen)
        self.screen = screen

    def get_boundaries(self, screen) -> list[Line]:
        s = screen
        w = screen.get_width()
        h = screen.get_height()
        shift = 10
        return [
            Line(Vector(shift, shift), Vector(shift, s.get_height() - shift)),
            Line(
                Vector(s.get_width() - shift, shift),
                Vector(s.get_width() - shift, s.get_height() - shift),
            ),
            Line(Vector(shift, shift), Vector(s.get_width() - shift, shift)),
            # Line(
            #     Vector(shift, s.get_height() - shift),
            #     Vector(s.get_width() - shift, s.get_height() - shift),
            # ),
            Line(
                Vector(w * 0.33, 0.9 * h),
                Vector(w * 0.33, 0.9 * h) + Vector(-1, -0.7).normalize() * 300,
            ),
            Line(
                Vector(w * 0.67, 0.9 * h),
                Vector(w * 0.67, 0.9 * h) + Vector(+1, -0.7).normalize() * 300,
            ),
        ]

    def draw(self):
        for l in self.boundaries:
            pygame.draw.line(
                self.screen, (255, 255, 255), (l.p1.x, l.p1.y), (l.p2.x, l.p2.y)
            )
