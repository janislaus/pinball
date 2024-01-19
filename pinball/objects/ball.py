from __future__ import annotations
import time
from copy import deepcopy
import math

from pinball.objects.line import Line

import pygame

from pinball.objects.vector import Vector
from pinball.objects.utils import (
    calculate_intersection,
    draw_lines,
)


class Ball:
    def __init__(self, pos: Vector, v: Vector, radius: float, colour):
        self.pos = pos
        self.radius = radius
        self.colour = colour
        self.v: Vector = v
        self.status = "in game"  # TODO: needed?
        self.old_pos = None
        self.old_v = None

    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, [self.pos.x, self.pos.y], self.radius)

    def move(self, boundaries: list[Line], gravity: float, dt: float):
        self.old_pos = self.pos
        self.old_v = self.v
        self.v.y += gravity * dt  # TODO: put it here?

        self.v = self.handle_collision(boundaries)

        self.pos.y += self.v.y * dt + gravity * dt**2
        self.pos.x += self.v.x * dt

    def handle_collision(self, boundaries: list[Line]) -> Vector:
        """
        Updates v if collision occurs.
        """
        nearest_boundary, nearest_point, distance_pos_boundary = calculate_metrics(
            boundaries, self.pos
        )

        collision_point = calculate_intersection(
            Line(self.pos, self.pos + self.v), nearest_boundary
        )

        if collision_point is not None:
            valid_collision = (distance_pos_boundary <= self.radius) and (
                nearest_boundary.contains(nearest_point)
            )

            tunneled = Line(self.pos, self.pos + self.v).contains(collision_point)

            ball_approaching = (self.pos - collision_point).magnitude > (
                self.pos + self.v.normalize() * 0.1 - collision_point
            ).magnitude

            if (valid_collision and ball_approaching) or tunneled:
                # if valid_collision and ball_approaching:
                print(nearest_boundary.v)
                return (
                    self.v.rotate(calculate_rotation_angle(self.v, nearest_boundary))
                    + nearest_boundary.v
                )

        return self.v


def calculate_nearest_point_on_line(line: Line, p: Vector) -> Vector:
    """
    Find nearest point on line to a given point p.
    """
    intersection = calculate_intersection(
        line, Line(p, Vector(-line.direction.y, line.direction.x))
    )
    if intersection is None:
        raise ValueError(
            "The lines are parallel, but this is impossible. There must be an error in calculate_intersection"
        )
    else:
        return intersection


def calculate_metrics(
    boundaries: list[Line], pos: Vector
) -> tuple[Line, Vector, float]:
    """
    Calculates the following metrics:
        - nearest boundary to pos
        - nearest line point on line to pos
        - distance between nearest point and pos

    """
    distances_to_boundaries = [
        (b, (pos - calculate_nearest_point_on_line(b, pos)).magnitude)
        for b in boundaries
    ]
    nearest_boundary, distance_pos_boundary = min(
        distances_to_boundaries, key=lambda x: x[1]
    )
    nearest_point = calculate_nearest_point_on_line(nearest_boundary, pos)

    return nearest_boundary, nearest_point, distance_pos_boundary


def calculate_rotation_angle(v: Vector, boundary: Line):
    """
    Calculates the rotation of v, for a collision with boundary.
    """
    angle = v.angle_with(boundary.direction)
    opposite_direction = angle >= (math.pi / 2)

    direction = boundary.direction if not opposite_direction else -boundary.direction
    incoming_angle = angle if not opposite_direction else math.pi - angle

    if v.cross_product(direction) < 0:
        return -2 * incoming_angle
    else:
        return 2 * incoming_angle
