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

        self.TOPICS = "course_topics"
        self.TOPICS_SQL = None

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
                               " (code, first, last, time) VALUES (%s, %s, %s, %s)"

        self.NEXT_QUARTER = prefix + self.NEXT_QUARTER
        self.NEXT_QUARTER_SQL = "INSERT INTO " + self.NEXT_QUARTER + \
                                " (code, first, last, time) VALUES (%s, %s, %s, %s)"

        self.TOPICS = prefix + self.TOPICS
        self.TOPICS_SQL = "INSERT INTO " + self.TOPICS + " (code, topic) " \
                          "VALUES (%s, %s)"

    def cleanup(self):
        self.db.truncate(self.MAIN)
        self.db.truncate(self.TERM)
        self.db.truncate(self.DEPT)
        self.db.truncate(self.CUR_QUARTER)
        self.db.truncate(self.NEXT_QUARTER)

    def publish_catalog(self, courses: List[Course]) -> None:
        results = []

        # topic_to_courses unused as of now, but if we want association tables
        # in memory instead of database we have it here for fast lookup
        course_to_topics, topic_to_courses = self.get_topics(courses)

        for course in courses:
            prereqs = "" if course.prereqs is None else course.prereqs
            data = (course.code.number, self.to_lower(course.name), course.units.min,
                    course.units.max, course.is_CRNC,
                    self.to_lower(prereqs), self.to_lower(course.desc))
            results.append(self.db.store(self.MAIN_SQL, data)) 

            for term in course.terms_offered:
                data = (course.code.number, self.to_lower(term.name))
                results.append(self.db.store(self.TERM_SQL, data))
               
            for dept in course.code.depts:
                data = (course.code.number, self.to_lower(dept))
                results.append(self.db.store(self.DEPT_SQL, data))

            for topic in course_to_topics[course.code.number]:
                data = (course.code.number, topic)
                results.append(self.db.store(self.TOPICS_SQL, data))

    def publish_schedule(self, courses: Tuple[Dict[int, List[Tuple[str, str]]],
                                              Dict[int, List[Tuple[str, str]]]]):
        cur_courses = courses[0]
        next_courses = courses[1]

        self.publish_quarter(cur_courses, self.CUR_QUARTER_SQL)
        self.publish_quarter(next_courses, self.NEXT_QUARTER_SQL)

    @staticmethod
    def get_topics(courses: List[Course]) -> Tuple[Dict[int: List[str]],
                                                   Dict[str: List[int]]]:
        """

        :param courses: List of course objects that contains the descriptions
                        and course numbers this method uses
        :return course_to_topics: Maps course number to its list of topics
        :return topic_to_courses: Maps topic to list of courses that reference it
        """
        NGRAMS = 3
        course_to_topics = {}
        topic_to_courses = {}

        for course in courses:
            word_list = course.desc.split(' ')
            for num_words in range(NGRAMS):
                for j in range(len(word_list) - num_words + 1):
                    ngram = '_'.join(word_list[j:j+num_words])
                    try:
                        course_to_topics[course.code.number].add(ngram)
                    except KeyError:
                        course_to_topics[course.code.number] = set()
                        course_to_topics[course.code.number].add(ngram)
                    try:
                        topic_to_courses[ngram].add(course.code.number)
                    except KeyError:
                        course_to_topics[ngram] = set()
                        course_to_topics[ngram].add(course.code.number)

        return course_to_topics, topic_to_courses

    def publish_quarter(self, quarter: Dict[int, List[Tuple[str, str]]], sql: str):
        results = []
        for code, sections in quarter.items():
            for section in sections:
                # Example section: ('Zoe J. Wood', 'TR 09:40 AM-11:00AM')
                name = section[0].split(' ')
                data = (code,
                        self.to_lower(name[0]),
                        self.to_lower(name[-1]),
                        section[1])
                results.append(self.db.store(sql, data))

    @staticmethod
    def to_lower(string):
        new_str = ""
        words = string.split(' ')
        for idx in range(len(words)):
            new_str = new_str + words[idx].lower()
            if idx < len(words) - 1 and len(words[idx + 1]) > 0:
                delimiter = "-" 
                if ord(words[idx + 1][0]) >= 65 and ord(words[idx + 1][0]) <= 90:
                   delimiter = "_"
                new_str = new_str + delimiter
        return new_str
