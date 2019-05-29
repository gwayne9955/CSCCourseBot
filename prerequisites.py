from typing import *
from enum import Enum, auto
from coursecode import CourseCode


class CourseCompletionRequirement(Enum):
    C_MINUS_OR_BETTER = auto()
    C_MINUS_OR_BETTER_OR_CONSENT_OF_INSTRUCTOR = auto()


class GEAreaCompletion:
    """
    Describes the prerequisite of the completion of a GE Area.
    """
    def __init__(self, area: str, requirement: Optional[CourseCompletionRequirement]):
        self.area = area
        self.requirement = requirement


class CourseCompletion:
    """
    Describes the prerequisite of the completion of a course.
    """
    def __init__(self, code: CourseCode, requirement: Optional[CourseCompletionRequirement]):
        self.code = code
        self.requirement = requirement


class ConsentOfInstructor:
    """
    Describes the prerequisite of instructor consent.
    This class serves only as a marker and has no fields.
    """
    def __init__(self):
        pass


class ClassStanding(Enum):
    """
    Describes a prerequisite of class standing.
    """
    SOPHOMORE = auto()
    JUNIOR = auto()
    GRADUATE = auto()


class PrerequisiteDisjunction:
    """
    Describes an 'or' relationship between multiple prerequisites.
    """
    def __init__(self, prerequisites):
        self.prerequisites = prerequisites


Prerequisite = Union[GEAreaCompletion, CourseCompletion, ConsentOfInstructor,
                     ClassStanding, PrerequisiteDisjunction]
"""
Describes a single prerequisite for enrolling in a course.
"""
