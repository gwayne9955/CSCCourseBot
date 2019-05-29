class CourseCode:
    """
    Describes a course code, which consists of a department abbreviation and a number.
    e.g. CSC 101
    """
    def __init__(self, dept: str, number: int):
        assert len(dept) == 3
        assert 100 < number < 600
        self.dept = dept
        self.code = number

    def __str__(self):
        return '{} {}'.format(self.dept, self.code)