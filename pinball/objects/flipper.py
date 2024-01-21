import math
from functools import partial
from time import time
from pinball.objects.line import Line
from pinball.objects.vector import Vector
import pygame
from constants import RIGHT_ROTATION_POINT, LEFT_ROTATION_POINT, SCREEN_WIDTH


class LeftFlipper:
    def __init__(self, screen, dt: float) -> None:
        self.screen = screen
        self.rotation_point = LEFT_ROTATION_POINT
        self.line = Line(
            self.rotation_point,
            self.rotation_point + Vector(1, 0.7).normalize() * SCREEN_WIDTH * 0.15,
            # Vector(w * 0.45, 0.95 * h),
        )
        self.state = "resting"
        self.angular_v = 0.25
        self.rotation_steps = int(math.pi / (3 * self.angular_v * dt))
        self.ctr = 0
        self.dt = dt
        self.rotation_direction = -1
        self.last_collision = float(0)

    @property
    def boundaries(self) -> list[Line]:
        if (time() - self.last_collision) > 0.5:
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
        self.rotation_point = RIGHT_ROTATION_POINT
        self.line = Line(
            self.rotation_point + Vector(-1, 0.7).normalize() * SCREEN_WIDTH * 0.15,
            self.rotation_point,
        )
        self.state = "resting"
        self.angular_v = 0.25
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


def calculate_distance(p1: Vector, p2: Vector):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)
