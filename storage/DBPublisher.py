from typing import *
from parser.course import Course
from storage.DBProxy import DBProxy


class DBPublisher:
    def __init__(self, db: DBProxy):
        self.db = db
        self.sql = "INSERT INTO courses (code, name, min_units, max_units" \
                   "term, is_crnc, prereqs, description) " \
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    def publish_courses(self, courses: List[Course]) -> None:
        results = []
        for course in courses:
            prereqs = "" if course.prereqs is None else course.prereqs
            for term in course.terms_offered:
                data = (course.code, course.name, course.units.min,
                        course.units.max, term.name, course.is_CRNC,
                        prereqs, course.desc)
                results.append(self.db.store(self.sql, data))
