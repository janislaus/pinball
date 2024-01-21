from __future__ import annotations
from functools import partial
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
    def __init__(self, pos: Vector, v: Vector, radius: float, colour, screen):
        self.pos = pos
        self.radius = radius
        self.colour = colour
        self.v: Vector = v
        self.status = "in game"  # TODO: needed?
        self.old_pos = None
        self.old_v = None
        self.screen = screen
        self.collision = False
        self.drawydraw = None

    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, [self.pos.x, self.pos.y], self.radius)

    def move(self, boundaries: list[Line], gravity: float, dt: float):
        self.old_pos = self.pos
        self.old_v = self.v
        self.v.y += gravity * dt  # TODO: put it here?

        self.v, self.collision = self.handle_collision(boundaries, dt)

        # if self.collision:
        #     self.draw(self.screen)
        #     self.drawydraw()
        #     pygame.display.flip()  # Update the display of the full screen
        #     pause()

        self.pos.y += self.v.y * dt + gravity * dt**2
        self.pos.x += self.v.x * dt

    def handle_collision(self, boundaries: list[Line], dt) -> tuple[Vector, bool]:
        """
        Updates v if collision occurs.
        """
        metrics = calculate_metrics(boundaries, self.pos)

        if metrics is None:
            return self.v, False

        nearest_boundary, nearest_point, distance_pos_boundary = metrics

        old_v = deepcopy(self.v)
        collision_point = calculate_intersection(
            Line(self.pos, self.pos + self.v), nearest_boundary
        )

        if collision_point is not None:
            valid_collision = distance_pos_boundary <= self.radius
            # and (
            # nearest_boundary.contains(nearest_point)
            # )

            tunneled = Line(self.pos, self.pos + self.v * dt).contains(collision_point)

            pygame.draw.circle(
                self.screen,
                (0, 0, 255),
                (nearest_point.x, nearest_point.y),
                5,
            )

            ball_approaching = (self.pos - collision_point).magnitude > (
                self.pos + self.v.normalize() * 0.1 - collision_point
            ).magnitude

            if tunneled:
                print("tunneled")
                if valid_collision and ball_approaching:
                    print("works anyways")

            if (valid_collision and ball_approaching) or tunneled:
                # if valid_collision and ball_approaching:
                boundary_v = nearest_boundary.v(collision_point=collision_point)
                print(boundary_v, boundary_v.magnitude)
                updated_v = (
                    self.v.rotate(calculate_rotation_angle(self.v, nearest_boundary))
                    + boundary_v
                )
                # ) + nearest_boundary.v(collision_point=collision_point)

                self.drawydraw = partial(
                    draw_collision,
                    ball=self,
                    nearest_boundary=nearest_boundary,
                    old_v=old_v,
                    updated_v=updated_v,
                    nearest_point=nearest_point,
                )

                return updated_v, True

        return self.v, False


def calculate_nearest_point_on_line(line: Line, p: Vector) -> Vector:
    """
    Find nearest point on line to a given point p.
    """
    intersection = calculate_intersection(
        line, Line(p, p + Vector(-line.direction.y, line.direction.x))
    )

    if intersection is None:
        raise ValueError(
            "The lines are parallel, but this is impossible. There must be an error in calculate_intersection"
        )
    else:
        return intersection


def calculate_metrics(
    boundaries: list[Line], pos: Vector
) -> tuple[Line, Vector, float] | None:
    """
    Calculates the following metrics:
        - nearest boundary to pos
        - nearest line point on line to pos
        - distance between nearest point and pos

    """
    valid_metrics = []
    for b in boundaries:
        nearest_point = calculate_nearest_point_on_line(b, pos)
        dist = (pos - nearest_point).magnitude

        if b.contains(nearest_point):
            valid_metrics.append((b, nearest_point, dist))

    if len(valid_metrics) == 0:
        return None
    return min(valid_metrics, key=lambda x: x[2])


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


def draw_collision(
    ball: Ball,
    nearest_boundary: Line,
    updated_v: Vector,
    old_v: Vector,
    nearest_point: Vector,
):
    factor = 2
    line_width = 5
    circle_r = 5

    pygame.draw.line(
        ball.screen,
        (255, 0, 0),
        (ball.pos.x, ball.pos.y),
        (ball.pos.x + factor * old_v.x, ball.pos.y + factor * old_v.y),
        width=line_width,
    )

    pygame.draw.circle(
        ball.screen,
        (255, 0, 0),
        (ball.pos.x + factor * old_v.x, ball.pos.y + factor * old_v.y),
        circle_r,
    )

    pygame.draw.line(
        ball.screen,
        (0, 255, 0),
        (ball.pos.x, ball.pos.y),
        (ball.pos.x + factor * updated_v.x, ball.pos.y + factor * updated_v.y),
        width=line_width,
    )

    pygame.draw.circle(
        ball.screen,
        (0, 255, 0),
        (ball.pos.x + factor * updated_v.x, ball.pos.y + factor * updated_v.y),
        circle_r,
    )

    pygame.draw.line(
        ball.screen,
        (255, 255, 255),
        (nearest_boundary.p1.x, nearest_boundary.p1.y),
        (nearest_boundary.p2.x, nearest_boundary.p2.y),
        width=line_width,
    )

    pygame.draw.circle(
        ball.screen,
        (255, 255, 255),
        (nearest_boundary.p2.x, nearest_boundary.p2.y),
        circle_r,
    )

    pygame.draw.circle(
        ball.screen,
        (0, 0, 255),
        (nearest_point.x, nearest_point.y),
        circle_r,
    )


def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                paused = False
