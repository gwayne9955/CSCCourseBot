from typing import *
from enum import Enum, auto
from parser.coursecode import CourseCode


class CourseCompletionRequirement(Enum):
    """
    Describes an additional requirement for fulfilling a course prerequisite.
    """
    C_MINUS_OR_BETTER = auto()
    C_MINUS_OR_BETTER_OR_CONSENT_OF_INSTRUCTOR = auto()


class GEAreaCompletion:
    """
    Describes the prerequisite of the completion of a GE Area.
    """
    def __init__(self, area: str, requirement: Optional[CourseCompletionRequirement]):
        self.area = area
        self.requirement = requirement

    def __eq__(self, other):
        return type(other) is GEAreaCompletion \
            and self.area == other.area \
            and self.requirement == other.requirement


class CourseCompletion:
    """
    Describes the prerequisite of the completion of a course.
    """
    def __init__(self, code: CourseCode, requirement: Optional[CourseCompletionRequirement]):
        self.code = code
        self.requirement = requirement

    def __eq__(self, other):
        return type(other) is CourseCompletion \
            and self.code == other.code \
            and self.requirement == other.requirement


class ConsentOfInstructor:
    """
    Describes the prerequisite of instructor consent.
    This class serves only as a marker and has no fields.
    """
    def __init__(self):
        pass

    def __eq__(self, other):
        return type(other) is ConsentOfInstructor


class ClassStanding(Enum):
    """
    Describes a prerequisite of class standing.
    """
    SOPHOMORE = auto()
    JUNIOR = auto()
    GRADUATE = auto()


MiscPrerequisite = str
"""
Describes a one-off miscellaneous prerequisite, 
e.g. Appropriate Math Placement Level.
"""


class PrerequisiteDisjunction:
    """
    Describes an 'or' relationship between multiple prerequisites.
    :param prerequisites: A list where each element is either
        - a prerequisite, or
        - a list of prerequisites, describing a conjunction
    """
    def __init__(self, prerequisites):
        self.prerequisites = prerequisites

    def __eq__(self, other):
        return type(other) is PrerequisiteDisjunction \
            and self.prerequisites == other.prerequisites


Prerequisite = Union[GEAreaCompletion, CourseCompletion, ConsentOfInstructor,
                     ClassStanding, MiscPrerequisite, PrerequisiteDisjunction]
"""
Describes a single prerequisite for enrolling in a course.
"""
