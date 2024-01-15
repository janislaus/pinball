from __future__ import annotations
from copy import deepcopy
import math

from pinball.objects.line import Line, rotate_line

from math import sin, cos
import pygame

from pinball.objects.point import Point
from pinball.objects.utils import (
    calculate_angle,
    calculate_distance,
    calculate_intersection,
    draw_lines,
)


class Ball:
    def __init__(self, x, y, r, colour, vx=0, vy=-0.1):
        self.pos = Point(x, y)
        self.radius = r
        self.colour = colour
        self.v: Point = Point(vx, vy)
        self.status = "in game"

    @property
    def v_line(self) -> Line:
        return Line(self.pos, self.pos + self.v)

    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, [self.pos.x, self.pos.y], self.radius)

    def move(self, GRAVITY_Y, DT, screen):
        self.v.y = self.v.y + GRAVITY_Y * DT
        # if self.pos.y +self.radius >= screen.get_height() or self.pos.y -self.radius <= 0:
        #     self.v.y *=-1
        if (
            self.pos.x + self.radius >= screen.get_width()
            or self.pos.x - self.radius <= 0
        ):
            self.v.x *= -1

        if self.pos.y >= screen.get_height() and (
            self.pos.x < ((screen.get_width() / 2) - 50)
            or self.pos.x > ((screen.get_width() / 2) + 50)
        ):
            self.v.y = self.v.y * (-1)

        self.pos.y = self.pos.y + self.v.y * DT + GRAVITY_Y * DT**2
        self.pos.x += self.v.x * DT

    def calculate_collision(self, object):
        """
        1) check if collision occurs : if distance from object is smaller than ball radius
        2) calculate the new velocity:
            - determine the angle between the object boundary and the velocity of the ball
            - determine the new velocity-vector:
                - determine the angle between x-axis and the object boundary
                - calculate the ausfallswinkel
                - determine x and y components of the velocity vector

        """
        object_boundaries: list[Line] = object.get_boundaries()
        # draw_lines(object_boundaries, legends=["1", "2", "3", "4"])

        info = []
        for line in object_boundaries:
            collision_point = calculate_intersection(
                Line(self.pos, self.pos + self.v), line
            )
            if collision_point is None:
                break

            distance = calculate_distance(self.pos, collision_point)

            valid_collision = line.contains(collision_point, self.radius) and (
                distance <= self.radius
            )
            if valid_collision:
                info.append((line, collision_point, distance))

        if info:
            line, collision_point, distance = max(info, key=lambda x: x[2])

            old = deepcopy(self.v_line)
            self.v = self.update_v(line)
            new = deepcopy(self.v_line)
            # draw_lines([old], legends=["old_v"])
            print(old == new)
            print(old)
            print(new)
            print("--------------")
            # draw_lines([old, new, line], legends=["old_v", "new_v", "boundary"])

    def update_v(self, boundary: Line):
        angle_incoming = calculate_angle(self.v_line, boundary)

        if self.v_line.angle < boundary.angle:
            new_v_line = rotate_line(self.v_line, math.pi - 2 * angle_incoming)
        else:
            new_v_line = rotate_line(self.v_line, -(math.pi - 2 * angle_incoming))

        new = new_v_line.p2 - new_v_line.p1
        return new
        # return Point(-new.x, -new.y)

        # draw_lines()
