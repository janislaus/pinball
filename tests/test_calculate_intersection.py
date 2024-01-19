from pinball.objects.line import Line
from pinball.objects.utils import calculate_intersection
from pinball.objects.vector import Vector


class CalculateIntersectionTests:
    def test_intersecting_lines(self):
        l1 = Line(Vector(0, 0), Vector(10, 10))
        l2 = Line(Vector(0, 10), Vector(10, 0))
        intersection = calculate_intersection(l1, l2)
        assert intersection == Vector(
            5, 5
        ), f"Intersection should be at (5, 5), got {intersection}"

    def test_parallel_lines(self):
        l1 = Line(Vector(0, 0), Vector(10, 10))
        l2 = Line(Vector(0, 1), Vector(10, 11))
        intersection = calculate_intersection(l1, l2)
        assert (
            intersection is None
        ), "There should be no intersection for parallel lines"

    def test_coincident_lines(self):
        l1 = Line(Vector(0, 0), Vector(10, 10))
        l2 = Line(Vector(0, 0), Vector(10, 10))
        intersection = calculate_intersection(l1, l2)
        assert (
            intersection is None
        ), "There should be no distinct intersection for coincident lines"

    def test_almost_parallel_lines(self):
        l1 = Line(Vector(0, 0), Vector(10, 10))
        l2 = Line(Vector(0, 0), Vector(10, 10.001))
        intersection = calculate_intersection(l1, l2)
        assert (
            intersection is not None
        ), "There should be an intersection for lines that are not exactly parallel"
