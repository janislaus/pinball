import math
import numpy as np
from pinball.objects.line import Line
from pinball.objects.vector import Vector
import pygame


class LeftFlipper:
    def __init__(self, screen, dt: float) -> None:
        self.screen = screen

        w = screen.get_width()
        h = screen.get_height()
        self.line = Line(Vector(w * 0.33, 0.9 * h), Vector(w * 0.45, 0.95 * h))
        self.state = "resting"
        self.angular_v = 0.5
        self.rotation_steps = int(math.pi / (4 * self.angular_v * dt))
        self.ctr = 0
        self.dt = dt
        self.rotation_direction = -1

    @property
    def boundaries(self) -> list[Line]:
        return [self.line]

    def draw(self):
        pygame.draw.line(
            self.screen,
            (0, 170, 255),
            (self.line.p1.x, self.line.p1.y),
            (self.line.p2.x, self.line.p2.y),
            width=15,
        )

    def update(self):
        if self.state == "hitting":
            self.hit()

    def hit(self):
        rotated_vector = self.line.direction.rotate(
            self.dt * self.rotation_direction * self.angular_v
        )

        self.ctr += 1
        if (self.ctr == self.rotation_steps) and (self.rotation_direction == -1):
            self.ctr = 0
            self.rotation_direction *= -1

        if (self.ctr == self.rotation_steps) and (self.rotation_direction == 1):
            self.ctr = 0
            self.rotation_direction *= -1
            self.state = "resting"

        self.line = Line(self.line.p1, self.line.p1 + rotated_vector)


class RightFlipper:
    def __init__(self, screen: pygame.surface.Surface, dt: float) -> None:
        self.screen = screen

        w = screen.get_width()
        h = screen.get_height()
        self.line = Line(Vector(w * 0.55, 0.95 * h), Vector(w * 0.67, 0.9 * h))
        self.state = "resting"
        self.angular_v = 0.5
        self.rotation_steps = int(math.pi / (4 * self.angular_v * dt))
        self.ctr = 0
        self.dt = dt
        self.rotation_direction = 1

    @property
    def boundaries(self) -> list[Line]:
        return [self.line]

    def draw(self):
        pygame.draw.line(
            self.screen,
            (0, 170, 255),
            (self.line.p1.x, self.line.p1.y),
            (self.line.p2.x, self.line.p2.y),
            width=15,
        )

    def update(self):
        if self.state == "hitting":
            self.hit()

    def hit(self):
        rotated_vector = self.line.direction.rotate(
            self.dt * self.rotation_direction * self.angular_v
        )

        self.ctr += 1
        if (self.ctr == self.rotation_steps) and (self.rotation_direction == 1):
            self.ctr = 0
            self.rotation_direction *= -1

        if (self.ctr == self.rotation_steps) and (self.rotation_direction == -1):
            self.ctr = 0
            self.rotation_direction *= -1
            self.state = "resting"

        self.line = Line(self.line.p2 - rotated_vector, self.line.p2)
