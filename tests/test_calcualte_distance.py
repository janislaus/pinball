from math import sqrt

from pinball.objects.vector import Vector

# Assuming Vector class is defined above


def calculate_distance(p1: Vector, p2: Vector):
    return sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


# Test cases
def test_calculate_distance():
    # Test with points at the same location
    p1 = Vector(0, 0)
    p2 = Vector(0, 0)
    assert (
        calculate_distance(p1, p2) == 0
    ), "Distance between identical points should be 0"

    # Test with points at unit distance horizontally
    p1 = Vector(0, 0)
    p2 = Vector(1, 0)
    assert calculate_distance(p1, p2) == 1, "Distance between these points should be 1"

    # Test with points at unit distance vertically
    p1 = Vector(0, 0)
    p2 = Vector(0, 1)
    assert calculate_distance(p1, p2) == 1, "Distance between these points should be 1"

    # Test with points diagonally (Pythagorean triplet)
    p1 = Vector(0, 0)
    p2 = Vector(3, 4)
    assert calculate_distance(p1, p2) == 5, "Distance between these points should be 5"

    # Test with negative coordinates
    p1 = Vector(-1, -1)
    p2 = Vector(-4, -5)
    assert calculate_distance(p1, p2) == 5, "Distance between these points should be 5"


# Run the tests
test_calculate_distance()
