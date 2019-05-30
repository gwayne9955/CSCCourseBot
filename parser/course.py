from typing import *
from parser.unitrange import UnitRange
from parser.coursecode import CourseCode
from parser.term import Term


class Course:
    def __init__(self, code: CourseCode, name: str, units: UnitRange, terms_offered: List[Term], is_CRNC: bool):
        self.code = code
        self.name = name
        self.units = units
        self.terms_offered = terms_offered
        self.is_CRNC = is_CRNC

    def __repr__(self):
        return 'Course(code = {}, name = {}, units = {}, terms_offered = {}, is_CRNC = {})'.format(self.code, self.name, self.units, self.terms_offered, self.is_CRNC)
