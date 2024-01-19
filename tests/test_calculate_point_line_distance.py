from pinball.objects.line import Line
from pinball.objects.vector import Vector
from pinball.objects.utils import calculate_intersection


def calculate_point_line_distance(line: Line, p: Vector) -> Vector:
    """
    Find nearest point on line to a given point p.
    """
    intersection = calculate_intersection(
        line, Line(p, Vector(-line.direction.y, line.direction.x))
    )
    if intersection:
        return intersection
        # return Line(p, intersection).length
    else:
        raise ValueError("WOGALO")
