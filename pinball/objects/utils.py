from __future__ import annotations
import matplotlib.pyplot as plt

import math
from pathlib import Path
from matplotlib.axes import Axes
from typing import TYPE_CHECKING
import random
import string

if TYPE_CHECKING:
    from pinball.objects.line import Line
from pinball.objects.point import Point
from math import acos, sqrt

plt.style.use("ggplot")


def calculate_distance(p1: Point, p2: Point):
    return sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def calculate_intersection(l1: Line, l2: Line) -> Point | None:
    if l1.angle == l2.angle:
        return None
    numerator = l1.direction.x * (l2.p1.y - l1.p1.y) + l1.direction.y * (
        l1.p1.x - l2.p1.x
    )
    denominator = l2.direction.x * l1.direction.y - l2.direction.y * l1.direction.x
    factor = numerator / denominator

    return Point(l2.p1.x + factor * l2.direction.x, l2.p1.y + factor * l2.direction.y)


def calculate_angle(l1: Line, l2: Line):
    return acos(
        (l1.direction.x * l2.direction.x + l1.direction.y * l2.direction.y)
        / (l1.length * l2.length)
    )


def random_string(length: int) -> str:
    """Generate a random string of specified length."""
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def draw_lines(lines: list[Line], legends: list[str]):
    ax: Axes
    _, ax = plt.subplots()  # type: ignore
    for line, legend in zip(lines, legends):
        line.create_plot(ax, legend)

    ax.set_aspect("equal", "box")
    ax.grid(True)
    plt.gca().invert_yaxis()
    plt.legend()
    path = Path(__file__).parents[2] / "data" / "collisions" / f"{random_string(5)}.png"
    plt.savefig(path)


def rotate_line(l: Line, angle: float) -> Line:
    rotated_point = Point(
        math.cos(angle) * l.p1.x - math.sin(angle) * l.p1.y,
        math.cos(angle) * l.p1.x + math.sin(angle) * l.p1.y,
    )
    return Line(l.p2, rotated_point)
