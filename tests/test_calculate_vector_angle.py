import math

from pinball.objects.vector import Vector, calculate_vector_angle


# Test class for the calculate_vector_angle function
class VectorAngleTests:
    def test_zero_angle(self):
        # Test with a vector along the positive x-axis
        vector = Vector(1, 0)
        assert math.isclose(
            calculate_vector_angle(vector), 0
        ), "Angle should be 0 for vector along x-axis"

    def test_positive_45_degree_angle(self):
        # Test with a vector at a 45-degree angle in the first quadrant
        vector = Vector(1, 1)
        assert math.isclose(
            calculate_vector_angle(vector), math.pi / 4
        ), "Angle should be π/4 for 45-degree vector"

    def test_negative_45_degree_angle(self):
        # Test with a vector at a -45-degree angle in the fourth quadrant
        vector = Vector(1, -1)
        assert math.isclose(
            calculate_vector_angle(vector), -math.pi / 4
        ), "Angle should be -π/4 for -45-degree vector"

    def test_90_degree_angle(self):
        # Test with a vector along the positive y-axis
        vector = Vector(0, 1)
        assert math.isclose(
            calculate_vector_angle(vector), math.pi / 2
        ), "Angle should be π/2 for vector along y-axis"

    def test_minus_90_degree_angle(self):
        # Test with a vector along the negative y-axis
        vector = Vector(0, -1)
        assert math.isclose(
            calculate_vector_angle(vector), -math.pi / 2
        ), "Angle should be -π/2 for vector along -y-axis"


# To run these tests, you would typically use a testing framework like pytest.
