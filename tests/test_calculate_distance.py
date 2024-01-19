from math import sqrt
from pinball.objects.utils import calculate_distance

from pinball.objects.vector import Vector


class CalculateDistanceTests:
    def test_calculate_distance(self):
        p1 = Vector(0, 0)
        p2 = Vector(0, 0)
        assert (
            calculate_distance(p1, p2) == 0
        ), "Distance between identical points should be 0"

        p1 = Vector(0, 0)
        p2 = Vector(1, 0)
        assert (
            calculate_distance(p1, p2) == 1
        ), "Distance between these points should be 1"

        p1 = Vector(0, 0)
        p2 = Vector(0, 1)
        assert (
            calculate_distance(p1, p2) == 1
        ), "Distance between these points should be 1"

        p1 = Vector(0, 0)
        p2 = Vector(3, 4)
        assert (
            calculate_distance(p1, p2) == 5
        ), "Distance between these points should be 5"

        p1 = Vector(-1, -1)
        p2 = Vector(-4, -5)
        assert (
            calculate_distance(p1, p2) == 5
        ), "Distance between these points should be 5"
