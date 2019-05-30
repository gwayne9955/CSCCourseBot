

class UnitRange:
    """
    Describes an inclusive range of units earned for taking a course.
    """
    def __init__(self, min: int, max: int):
        assert min >= 1
        assert max >= min
        self.min = min
        self.max = max

    @staticmethod
    def always(units):
        return UnitRange(units, units)

    def __str__(self):
        if self.min == self.max:
            return str(self.min)
        else:
            return '{}-{}'.format(self.min, self.max)
