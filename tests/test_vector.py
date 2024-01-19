from pinball.objects.vector import Vector
import math
import pytest


class VectorTests:
    def test_addition(self):
        v1 = Vector(1, 2)
        v2 = Vector(3, 4)
        result = v1 + v2
        result2 = v2 + v1
        assert result == Vector(4, 6), f"Expected Vector(4, 6), got {result}"
        assert result2 == Vector(4, 6), f"Expected Vector(4, 6), got {result2}"

    def test_subtraction(self):
        v1 = Vector(1, 2)
        v2 = Vector(3, 4)
        result = v1 - v2
        result2 = v2 - v1
        assert result == Vector(-2, -2), f"Expected Vector(-2, -2), got {result}"
        assert result2 == Vector(2, 2), f"Expected Vector(2, 2), got {result2}"

    def test_multiplication(self):
        v1 = Vector(1, 2)
        result = v1 * 3
        result2 = 3 * v1
        result3 = -v1
        assert result == Vector(3, 6), f"Expected Vector(3, 6), got {result}"
        assert result2 == Vector(3, 6), f"Expected Vector(3, 6), got {result2}"
        assert result3 == Vector(-1, -2), f"Expected Vector(-1, -2), got {result3}"

    def test_dot_product(self):
        v1 = Vector(1, 2)
        v2 = Vector(3, 2)
        v3 = Vector(3, -2)
        result = v1 @ v2
        result2 = v2 @ v1
        result3 = v1 @ v3
        result4 = v3 @ v1
        assert result == 7, f"Expected 7, got {result}"
        assert result2 == 7, f"Expected 7, got {result2}"
        assert result3 == -1, f"Expected -1, got {result3}"
        assert result4 == -1, f"Expected -1, got {result4}"

    def test_division(self):
        v1 = Vector(4, 8)
        result = v1 / 2
        result2 = v1 / -2
        assert result == Vector(2, 4), f"Expected Vector(2, 4), got {result}"
        assert result2 == Vector(-2, -4), f"Expected Vector(-2, -4), got {result2}"

    def test_rotate(self):
        v = Vector(1, 0)

        v_rotated = v.rotate(0)
        assert math.isclose(v_rotated.x, 1, abs_tol=1e-7) and math.isclose(
            v_rotated.y, 0, abs_tol=1e-7
        )

        v_rotated = v.rotate(math.pi / 2)
        assert math.isclose(v_rotated.x, 0, abs_tol=1e-7) and math.isclose(
            v_rotated.y, 1, abs_tol=1e-7
        )

        v_rotated = v.rotate(math.pi)
        assert math.isclose(v_rotated.x, -1, abs_tol=1e-7) and math.isclose(
            v_rotated.y, 0, abs_tol=1e-7
        )

        v_rotated = v.rotate(3 * math.pi / 2)
        assert math.isclose(v_rotated.x, 0, abs_tol=1e-7) and math.isclose(
            v_rotated.y, -1, abs_tol=1e-7
        )

        v_rotated = v.rotate(-math.pi / 2)
        assert math.isclose(v_rotated.x, 0, abs_tol=1e-7) and math.isclose(
            v_rotated.y, -1, abs_tol=1e-7
        )

    def test_magnitude(self):
        v = Vector(0, 0)
        assert math.isclose(v.magnitude, 0, abs_tol=1e-7)

        v = Vector(1, 0)
        assert math.isclose(v.magnitude, 1, abs_tol=1e-7)

        v = Vector(0, 1)
        assert math.isclose(v.magnitude, 1, abs_tol=1e-7)

        v = Vector(3, 4)  # 3-4-5 right triangle
        assert math.isclose(v.magnitude, 5, abs_tol=1e-7)

        v = Vector(-3, -4)
        assert math.isclose(v.magnitude, 5, abs_tol=1e-7)

    def test_normalize(self):
        # Normalizing a non-zero vector
        v = Vector(3, 4)
        v_normalized = v.normalize()
        assert math.isclose(v_normalized.magnitude, 1, abs_tol=1e-7)
        assert math.isclose(v_normalized.x, 3 / 5, abs_tol=1e-7) and math.isclose(
            v_normalized.y, 4 / 5, abs_tol=1e-7
        )

        # Normalizing a unit vector (should remain unchanged)
        v = Vector(1, 0)
        v_normalized = v.normalize()
        assert math.isclose(v_normalized.magnitude, 1, abs_tol=1e-7)
        assert math.isclose(v_normalized.x, 1, abs_tol=1e-7) and math.isclose(
            v_normalized.y, 0, abs_tol=1e-7
        )

        # Normalizing a vector with negative components
        v = Vector(-3, -4)
        v_normalized = v.normalize()
        assert math.isclose(v_normalized.magnitude, 1, abs_tol=1e-7)
        assert math.isclose(v_normalized.x, -3 / 5, abs_tol=1e-7) and math.isclose(
            v_normalized.y, -4 / 5, abs_tol=1e-7
        )

        # Edge case: Normalizing a zero vector should raise an error
        v = Vector(0, 0)
        with pytest.raises(ZeroDivisionError):
            v.normalize()

    def test_angle_with(self):
        # Angle with the same vector (should be 0)
        v1 = Vector(1, 0)
        assert math.isclose(v1.angle_with(v1), 0, abs_tol=1e-7)

        # Angle with orthogonal vector (should be 90 degrees)
        v2 = Vector(0, 1)
        assert math.isclose(v1.angle_with(v2), math.pi / 2, abs_tol=1e-7)

        # Angle with opposite vector (should be 180 degrees)
        v3 = Vector(-1, 0)
        assert math.isclose(v1.angle_with(v3), math.pi, abs_tol=1e-7)

        # Angle with another vector at 45 degrees
        v4 = Vector(1, 1)
        assert math.isclose(v1.angle_with(v4), math.pi / 4, abs_tol=1e-7)

        # Edge case: Angle with a zero vector should raise an error
        v_zero = Vector(0, 0)
        with pytest.raises(ZeroDivisionError):
            v1.angle_with(v_zero)
