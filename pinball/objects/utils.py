from __future__ import annotations
import matplotlib.pyplot as plt
import time

import math
from pathlib import Path
from matplotlib.axes import Axes
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pinball.objects.line import Line
from pinball.objects.vector import Vector
from math import sqrt

plt.style.use("ggplot")


def calculate_distance(p1: Vector, p2: Vector):
    return sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


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


def draw_lines(lines: list[Line], legends: list[str] | None = None):
    if legends is None:
        legends = [""] * len(lines)

    ax: Axes
    _, ax = plt.subplots()  # type: ignore

    for line, legend in zip(lines, legends):
        line.create_plot(ax, legend)

    ax.set_aspect("equal", "box")
    ax.grid(True)
    plt.gca().invert_yaxis()
    plt.legend()
    path = Path(__file__).parents[2] / "data" / "collisions" / f"{time.time()}.png"
    plt.savefig(path, dpi=400)
