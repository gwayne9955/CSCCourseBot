from typing import *
from parser.unitrange import UnitRange
from parser.coursecode import CourseCode
from parser.term import Term


class Course:
    def __init__(self, code: CourseCode, name: str, units: UnitRange,
                 terms_offered: List[Term], is_CRNC: bool,
                 prereqs: Optional[str], desc: str):
        self.code = code
        self.name = name
        self.units = units
        self.terms_offered = terms_offered
        self.is_CRNC = is_CRNC
        self.prereqs = prereqs
        self.desc = desc

    def __repr__(self):
        return 'Course(code = {}, ' \
               'name = {}, ' \
               'units = {}, ' \
               'terms_offered = {}, ' \
               'is_CRNC = {}, ' \
               'prereqs = {}' \
               'desc = {})'.format(self.code,
                                   self.name,
                                   self.units,
                                   self.terms_offered,
                                   self.is_CRNC,
                                   self.prereqs,
                                   self.desc)
