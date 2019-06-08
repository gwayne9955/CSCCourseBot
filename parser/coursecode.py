class CourseCode:
    """
    Describes a course code, which consists of one or two department abbreviations and a number.
    e.g. CSC 101, CPE/CSC 357
    """
    def __init__(self, dept: str, number: int):
        assert 100 <= number < 600
        self.depts = tuple(dept.split('/'))
        assert len(self.depts) in [1, 2]
        assert all(len(dept) in range(2, 5) for dept in self.depts)
        self.number = number

    def __eq__(self, other):
        return type(other) is CourseCode \
               and self.depts == other.depts \
               and self.number == other.number

    def __hash__(self):
        return hash(self.number)

    def __str__(self):
        return '{} {}'.format('/'.join(self.depts), self.number)
