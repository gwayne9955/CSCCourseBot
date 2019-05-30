from enum import Enum, unique


@unique
class Term(Enum):
    FALL = 'F'
    WINTER = 'W'
    SPRING = 'SP'
    INDETERMINATE = 'TBD'

    @staticmethod
    def from_str(string: str):
        for term in Term:
            if term.value == string:
                return term
        assert False, 'Cannot initialize term from {}'.format(string)

    def __repr__(self):
        return self.name
