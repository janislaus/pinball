from __future__ import annotations
import math
from pinball.objects.vector import Vector, calculate_vector_angle
from pinball.objects.utils import calculate_distance, draw_lines
from matplotlib.axes import Axes


class Line:
    def __init__(self, p1: Vector, p2: Vector) -> None:
        self.p1: Vector = p1
        self.p2: Vector = p2
        self.direction: Vector = p2 - p1
        self.length: float = calculate_distance(self.p1, self.p2)
        if self.direction.x == 0:
            self.angle = math.pi / 2
        else:
            self.angle = calculate_vector_angle(self.direction)

    def __repr__(self) -> str:
        return f"Point1: {self.p1}, Point2: {self.p2}"

    def __str__(self) -> str:
        return f"Point1: {self.p1}, Point2: {self.p2}"

    def __eq__(self, other: Line) -> bool:
        return (self.p1 == other.p1) and (self.p2 == other.p2)

    def contains(self, p: Vector) -> bool:
        if point_on_line(self, p):
            in_x_range = (
                (min([self.p1.x, self.p2.x])) <= p.x <= (max([self.p1.x, self.p2.x]))
            )
            in_y_range = (
                (min([self.p1.y, self.p2.y])) <= p.y <= (max([self.p1.y, self.p2.y]))
            )
            return in_x_range and in_y_range
        else:
            return False

    def create_plot(self, ax: Axes, label=None):
        ax.plot([self.p1.x, self.p2.x], [self.p1.y, self.p2.y], label=label)
        ax.arrow(
            self.p1.x,
            self.p1.y,
            self.direction.x,
            self.direction.y,
            head_width=50,
            head_length=50,
            fc="black",
            ec="black",
        )


def point_on_line(line: Line, p: Vector) -> bool:
    return math.isclose(
        (p.x - line.p1.x) * line.direction.y, (p.y - line.p1.y) * line.direction.x
    )
