import math
from typing import Callable
from pinball.objects.vector import Vector
from matplotlib.axes import Axes


def calculate_default_collision_v(collision_point: Vector) -> Vector:
    return Vector(0, 0)


class Line:
    def __init__(self, p1: Vector, p2: Vector, v=calculate_default_collision_v) -> None:
        self.p1: Vector = p1
        self.p2: Vector = p2
        self.v: Callable[..., Vector] = v
        self.direction: Vector = p2 - p1

    def __repr__(self) -> str:
        return f"Point1: {self.p1}, Point2: {self.p2}"

    def __str__(self) -> str:
        return f"Point1: {self.p1}, Point2: {self.p2}"

    def __eq__(self, other) -> bool:
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


def lines_parallel(l1: Line, l2: Line) -> bool:
    """
    Lines are parallel if the cross product of their direction vectors is 0.
    """
    return math.isclose(l1.direction.cross_product(l2.direction), 0, abs_tol=1e-7)


def calculate_intersection(l1: Line, l2: Line) -> Vector | None:
    if lines_parallel(l1, l2):
        return None

    numerator = l1.direction.x * (l2.p1.y - l1.p1.y) + l1.direction.y * (
        l1.p1.x - l2.p1.x
    )
    denominator = l2.direction.x * l1.direction.y - l2.direction.y * l1.direction.x
    factor = numerator / denominator

    return Vector(l2.p1.x + factor * l2.direction.x, l2.p1.y + factor * l2.direction.y)
