from typing import *
from parser.course import Course
from storage.DBProxy import DBProxy


class DBPublisher:
    def __init__(self, db: DBProxy):
        self.db = db

        self.MAIN = "main_courses" 
        self.MAIN_SQL = "INSERT INTO " + self.MAIN + " (code, name, min_units, max_units," \
                        "is_crnc, prereqs, description) " \
                        "VALUES (%s, %s, %s, %s, %s, %s, %s)"

        self.TERM = "course_terms"
        self.TERM_SQL = "INSERT INTO " + self.TERM + " (code, term) " \
                        "VALUES (%s, %s)"

        self.DEPT = "course_depts"
        self.DEPT_SQL = "INSERT INTO " + self.DEPT + " (code, department) " \
                        "VALUES (%s, %s)"

    def set_table_prefix(self, prefix: str) -> None:
        self.MAIN = prefix + "_main_courses" 
        self.MAIN_SQL = "INSERT INTO " + self.MAIN + " (code, name, min_units, max_units," \
                        "is_crnc, prereqs, description) " \
                        "VALUES (%s, %s, %s, %s, %s, %s, %s)"

        self.TERM = prefix + "_course_terms" 
        self.TERM_SQL = "INSERT INTO " + self.TERM + " (code, term) " \
                        "VALUES (%s, %s)"

        self.DEPT = prefix + "_course_depts"
        self.DEPT_SQL = "INSERT INTO " + self.DEPT + " (code, department) " \
                        "VALUES (%s, %s)"

    def cleanup(self):
        self.db.truncate(self.MAIN)
        self.db.truncate(self.TERM)
        self.db.truncate(self.DEPT)

    def publish_courses(self, courses: List[Course]) -> None:
        results = []
        for course in courses:
            prereqs = "" if course.prereqs is None else course.prereqs
            data = (course.code.number, self.to_lower(course.name), course.units.min,
                    course.units.max, course.is_CRNC,
                    self.to_lower(prereqs), self.to_lower(course.desc))
            results.append(self.db.store(self.MAIN_SQL, data)) 

            for term in course.terms_offered:
                data = (course.code.number, term.name)
                results.append(self.db.store(self.TERM_SQL, data))
               
            for dept in course.code.depts:
                data = (course.code.number, dept)
                results.append(self.db.store(self.DEPT_SQL, data))

    @staticmethod
    def to_lower(string):
        new_str = ""
        words = string.split(' ')
        for idx in range(len(words)):
            new_str = new_str + words[idx].lower()
            if idx < len(words) - 1 and len(words[idx + 1]) > 0:
                delimiter = "-" 
                if ord(words[idx + 1][0]):
                   delimiter = "_"
                new_str = new_str + delimiter
        return new_str
