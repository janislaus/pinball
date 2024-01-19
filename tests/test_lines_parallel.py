from pinball.objects.line import Line
from pinball.objects.utils import lines_parallel
from pinball.objects.vector import Vector


class LinesParallelTests:
    def test_parallel_lines(self):
        l1 = Line(Vector(0, 0), Vector(10, 10))
        l2 = Line(Vector(5, 5), Vector(15, 15))
        assert lines_parallel(l1, l2), "Lines should be parallel"

    def test_non_parallel_lines(self):
        l1 = Line(Vector(0, 0), Vector(10, 10))
        l2 = Line(Vector(0, 0), Vector(10, 5))
        assert not lines_parallel(l1, l2), "Lines should not be parallel"

    def test_perpendicular_lines(self):
        l1 = Line(Vector(0, 0), Vector(10, 0))
        l2 = Line(Vector(0, 0), Vector(0, 10))
        assert not lines_parallel(l1, l2), "Lines should not be parallel"

    def test_parallel_opposite_direction_lines(self):
        l1 = Line(Vector(0, 0), Vector(10, 10))
        l2 = Line(Vector(10, 10), Vector(0, 0))
        assert lines_parallel(l1, l2), "Lines should be parallel"

    def test_almost_parallel_lines(self):
        l1 = Line(Vector(0, 0), Vector(10, 10))
        l2 = Line(Vector(0, 0), Vector(10, 10.000001))
        assert not lines_parallel(l1, l2), "Lines should not be parallel"
