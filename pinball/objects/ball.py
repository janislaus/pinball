from __future__ import annotations
import math

from pinball.objects.line import Line, rotate_line

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

    def calculate_collision(self, boundaries: list[Line], gravity: float, dt: float):
        collisions = []
        for boundary in boundaries:
            collision_point = calculate_intersection(
                Line(self.pos, self.pos + self.v), boundary
            )
            if collision_point is None:
                continue

            distance = calculate_distance(self.pos, collision_point)

            intersection = calculate_point_line_distance(boundary, self.pos)
            closest_distance = Line(self.pos, intersection).length

            valid_collision = (closest_distance <= self.radius) and (
                boundary.contains(intersection, radius=30)
            )
            if valid_collision:
                collisions.append(
                    (boundary, collision_point, distance, closest_distance)
                )

        if collisions:
            # TODO: check this
            boundary, collision_point, distance, closest_distance = min(
                collisions, key=lambda x: x[3]
            )

            # TODO: this is not correct, if the velocity is other than perpendicular to the boundary line
            # self.pos = self.adjust_position(distance=distance)
            self.v = self.update_v(boundary)

        self.v.y += gravity * dt
        self.pos.y += self.v.y * dt + gravity * dt**2
        self.pos.x += self.v.x * dt

    def update_v(self, boundary: Line):
        angle_incoming = calculate_angle(self.v_line, boundary)

        if self.v_line.angle > boundary.angle:
            new_v_line = rotate_line(self.v_line, math.pi - 2 * angle_incoming)
        else:
            new_v_line = rotate_line(self.v_line, -(math.pi - 2 * angle_incoming))

        # new = new_v_line.p2 - new_v_line.p1
        # new = new_v_line.p2 - new_v_line.p1
        return new_v_line.direction

    def adjust_position(self, distance: float):
        direction_unit_vector = self.v_line.direction / self.v_line.length
        return self.pos + direction_unit_vector * (-1) * (self.radius - distance)


def calculate_point_line_distance(line: Line, p: Point) -> Point:
    """
    Find nearest point on line to a given point p.
    """
    intersection = calculate_intersection(
        line, Line(p, Point(-line.direction.y, line.direction.x))
    )
    if intersection:
        return intersection
        # return Line(p, intersection).length
    else:
        raise ValueError("WOGALO")
