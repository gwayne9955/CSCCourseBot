from typing import *
from parser.course import Course
from parser.schedulecourse import ScheduleCourse
from storage.DBProxy import DBProxy


class DBPublisher:
    def __init__(self, db: DBProxy):
        self.db = db

        self.MAIN = "main_courses" 
        self.MAIN_SQL = None

        self.TERM = "course_terms"
        self.TERM_SQL = None

        self.DEPT = "course_depts"
        self.DEPT_SQL = None

        self.CUR_QUARTER = "cur_schedule"
        self.CUR_QUARTER_SQL = None

        self.NEXT_QUARTER = "next_schedule"
        self.NEXT_QUARTER_SQL = None

        self.set_table_prefix("")

    def set_table_prefix(self, prefix: str) -> None:
        self.MAIN = prefix + self.MAIN
        self.MAIN_SQL = "INSERT INTO " + self.MAIN + " (code, name, min_units, max_units," \
                        "is_crnc, prereqs, description) " \
                        "VALUES (%s, %s, %s, %s, %s, %s, %s)"

        self.TERM = prefix + self.TERM
        self.TERM_SQL = "INSERT INTO " + self.TERM + " (code, term) " \
                        "VALUES (%s, %s)"

        self.DEPT = prefix + self.DEPT
        self.DEPT_SQL = "INSERT INTO " + self.DEPT + " (code, department) " \
                        "VALUES (%s, %s)"

        self.CUR_QUARTER = prefix + self.CUR_QUARTER
        self.CUR_QUARTER_SQL = "INSERT INTO " + self.CUR_QUARTER + \
                               " (code, professor, time) VALUES (%s, %s, %s)"

        self.NEXT_QUARTER = prefix + self.NEXT_QUARTER
        self.NEXT_QUARTER_SQL = "INSERT INTO " + self.NEXT_QUARTER + \
                                " (code, professor, time) VALUES (%s, %s, %s)"

    def cleanup(self):
        self.db.truncate(self.MAIN)
        self.db.truncate(self.TERM)
        self.db.truncate(self.DEPT)

    def publish_catalog(self, courses: List[Course]) -> None:
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

    def publish_schedule(self, courses: Tuple[Dict[int, List[Tuple[str, str]]],
                                              Dict[int, List[Tuple[str, str]]]]):
        results = []

        cur_courses = courses[0]
        next_courses = courses[1]

        for code, sections in cur_courses.items():
            for section in sections:
                # Example section: ('Foaad Khosmood', 'TR 12:10 PM- 1:30PM')
                data = (code, section[0], section[1])
                results.append(self.db.store(self.CUR_QUARTER_SQL, data))

        for code, sections in next_courses.items():
            for section in sections:
                # Example section: ('Foaad Khosmood', 'TR 12:10 PM- 1:30PM')
                data = (code, section[0], section[1])
                results.append(self.db.store(self.NEXT_QUARTER_SQL, data))

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
