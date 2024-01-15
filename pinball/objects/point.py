from __future__ import annotations


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: Point) -> bool:
        return (self.x == other.x) and (self.y == other.y)

    def __repr__(self) -> str:
        return f"x: {self.x}, y: {self.y}"

    def __str__(self) -> str:
        return f"x: {self.x}, y: {self.y}"

    def __add__(self: Point, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self: Point, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)
