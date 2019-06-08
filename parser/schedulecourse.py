from typing import *
from parser.coursecode import CourseCode


class ScheduleCourse:
    def __init__(self, code: CourseCode, time: str, prof_name: str):
        self.code = code
        self.time = time
        self.prof_name = prof_name

    def __repr__(self):
        return "{} {} {}".format(self.prof_name.split(' ')[-1], self.code,
                                 self.time)
