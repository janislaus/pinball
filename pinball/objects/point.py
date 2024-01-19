from __future__ import annotations
import math


class Vector:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: Vector) -> bool:
        return (self.x == other.x) and (self.y == other.y)

    def __repr__(self) -> str:
        return f"x: {self.x}, y: {self.y}"

    def __str__(self) -> str:
        return f"x: {self.x}, y: {self.y}"

    def __add__(self: Vector, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self: Vector, other: Vector) -> Vector:
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self: Vector, other: float) -> Vector:
        return Vector(self.x * other, self.y * other)

    def __truediv__(self: Vector, other: float) -> Vector:
        return Vector(self.x / other, self.y / other)


def calculate_vector_angle(vector: Vector):
    """
    Calculate angle between x-Axis and Vector.
    """
    return math.atan(vector.y / vector.x)
