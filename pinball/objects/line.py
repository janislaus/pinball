from __future__ import annotations
import math
from pinball.objects.point import Point
from pinball.objects.utils import calculate_distance, draw_lines
from matplotlib.axes import Axes


class Line:
    def __init__(self, p1: Point, p2: Point) -> None:
        self.p1 = p1
        self.p2 = p2
        self.length = calculate_distance(self.p1, self.p2)
        self.direction = p2 - p1
        if self.direction.x == 0:
            self.angle = math.pi / 2
        else:
            self.angle = math.atan(self.direction.y / self.direction.x)

    def __repr__(self) -> str:
        return f"Point1: {self.p1}, Point2: {self.p2}"

    def __str__(self) -> str:
        return f"Point1: {self.p1}, Point2: {self.p2}"

    def __eq__(self, other: Line) -> bool:
        return (self.p1 == other.p1) and (self.p2 == other.p2)

    def contains(self, p: Point, radius: float) -> bool:
        if math.isclose(
            (p.x - self.p1.x) * self.direction.y, (p.y - self.p1.y) * self.direction.x
        ):
            in_x_range = (
                (min([self.p1.x, self.p2.x]) - radius)
                <= p.x
                <= (max([self.p1.x, self.p2.x]) + radius)
            )
            in_y_range = (
                (min([self.p1.y, self.p2.y]) - radius)
                <= p.y
                <= (max([self.p1.y, self.p2.y]) + radius)
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
            head_width=1,
            head_length=1,
            fc="black",
            ec="black",
        )


def rotate_line(l: Line, angle: float) -> Line:
    rotated_point = Point(
        math.cos(angle) * (-1) * l.direction.x - math.sin(angle) * (-1) * l.direction.y,
        math.cos(angle) * (-1) * l.direction.y + math.sin(angle) * (-1) * l.direction.x,
    )
    return Line(l.p2, l.p2 + rotated_point)


if __name__ == "__main__":
    l = Line(Point(2, 2), Point(1, 1))
    l2 = rotate_line(l, math.pi / 2)
    draw_lines([l, l2], ["l", "l2"])
    print("SUCCESS")
