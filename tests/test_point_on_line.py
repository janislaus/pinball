from pinball.objects.line import Line, point_on_line
from pinball.objects.vector import Vector


class PointOnLineTests:
    def test_point_on_line(self):
        p1 = Vector(0, 0)
        p2 = Vector(10, 10)
        line = Line(p1, p2)

        # Test with a point on the line
        p_on_line = Vector(5, 5)
        assert point_on_line(line, p_on_line), "Point should be on the line"

        # Test with a point not on the line
        p_off_line = Vector(5, 6)
        assert not point_on_line(line, p_off_line), "Point should not be on the line"

        # Test with line endpoints
        assert point_on_line(line, p1), "Line endpoint should be on the line"
        assert point_on_line(line, p2), "Line endpoint should be on the line"
