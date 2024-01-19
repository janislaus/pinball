from __future__ import annotations
import math


class Vector:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def cross_product(self, other: "Vector") -> float:
        return self.x * other.y - self.y * other.x

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

    def __rmul__(self, other: float) -> Vector:
        return Vector(self.x * other, self.y * other)

    def __neg__(self) -> Vector:
        return Vector(-self.x, -self.y)

    def __truediv__(self: Vector, other: float) -> Vector:
        if other == 0:
            raise ValueError("Cannot divide by zero")
        return Vector(self.x / other, self.y / other)

    def __matmul__(self, other: "Vector") -> float:
        return self.x * other.x + self.y * other.y

    def rotate(self, angle: float) -> Vector:
        """
        rotates counter clockwise
        """
        cos_angle, sin_angle = math.cos(angle), math.sin(angle)
        return Vector(
            self.x * cos_angle - self.y * sin_angle,
            self.x * sin_angle + self.y * cos_angle,
        )

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self) -> Vector:
        mag = self.magnitude
        return Vector(self.x / mag, self.y / mag)

    def angle_with(self, other: Vector) -> float:
        dot_product = self @ other
        return math.acos(dot_product / (self.magnitude * other.magnitude))


def calculate_vector_angle(vector: Vector):
    """
    Calculate angle between x-Axis and Vector.
    """
    return math.atan2(vector.y, vector.x)
