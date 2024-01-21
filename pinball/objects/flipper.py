import math
from functools import partial
from time import time
import numpy as np
from pinball.objects.line import Line
from pinball.objects.utils import calculate_distance
from pinball.objects.vector import Vector
import pygame


class LeftFlipper:
    def __init__(self, screen, dt: float) -> None:
        self.screen = screen

        w = screen.get_width()
        h = screen.get_height()
        self.rotation_point = Vector(w * 0.33, 0.9 * h)
        self.line = Line(
            self.rotation_point,
            self.rotation_point + Vector(1, 0.7).normalize() * w * 0.15,
            # Vector(w * 0.45, 0.95 * h),
        )
        self.state = "resting"
        self.angular_v = 0.3
        self.rotation_steps = int(math.pi / (3 * self.angular_v * dt))
        self.ctr = 0
        self.dt = dt
        self.rotation_direction = -1
        self.last_collision = float(0)

    @property
    def boundaries(self) -> list[Line]:
        if (time() - self.last_collision) > 0.3:
            return [
                Line(
                    self.line.p1,
                    self.line.p2,
                    v=partial(calculate_flipper_v, flipper=self),
                )
            ]
        else:
            return []

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
        self.rotation_point = Vector(w * 0.67, 0.9 * h)
        self.line = Line(
            # Vector(w * 0.55, 0.95 * h),
            self.rotation_point + Vector(-1, 0.7).normalize() * w * 0.15,
            self.rotation_point,
        )
        self.state = "resting"
        self.angular_v = 0.5
        self.rotation_steps = int(math.pi / (3 * self.angular_v * dt))
        self.ctr = 0
        self.dt = dt
        self.rotation_direction = 1
        self.last_collision = float(0)

    @property
    def boundaries(self) -> list[Line]:
        if (time() - self.last_collision) > 0.3:
            return [
                Line(
                    self.line.p1,
                    self.line.p2,
                    v=partial(calculate_flipper_v, flipper=self),
                )
            ]
        else:
            return []

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


def calculate_flipper_v(
    collision_point: Vector, flipper: LeftFlipper | RightFlipper
) -> Vector:
    if flipper.state != "hitting":
        return Vector(0, 0)
    else:
        flipper.last_collision = time()
        factor = (
            calculate_distance(collision_point, flipper.rotation_point)
            / flipper.line.direction.magnitude
        )
        direction = -Vector(
            -flipper.line.direction.y, flipper.line.direction.x
        ).normalize()

        return 20 * factor * direction
