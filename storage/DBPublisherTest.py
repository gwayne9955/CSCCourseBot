import unittest

from parser.course import Course
from parser.coursecode import CourseCode
from parser.term import Term
from parser.unitrange import UnitRange

from storage.DBProxy import DBProxy
from storage.DBPublisher import DBPublisher


class TestDBPublisher(unittest.TestCase):

    # Wet run test, will add to database on Frank
    def test_publish_courses(self):
        test_course_code = CourseCode("CSC", 466)
        test_couse_name = "Knowledge Discovery from Data"
        test_unit_range = UnitRange(1, 4)
        test_terms = [Term.from_str("F"), Term.from_str("SP")]
        test_iscrnc = 0
        test_prereqs = "CSC 349 and one of the following: STAT 302, STAT 312, " \
                       "STAT 321 or STAT 350."
        test_desc = "Overview of modern knowledge discovery from data (KDD) " \
                    "methods and technologies. Topics in data mining " \
                    "(association rules mining, classification, clustering), " \
                    "information retrieval, web mining. Emphasis on use of KDD " \
                    "techniques in modern software applications. 3 lectures, " \
                    "1 laboratory."

        test_courses = [Course(test_course_code,
                               test_couse_name,
                               test_unit_range,
                               test_terms,
                               test_iscrnc,
                               test_prereqs,
                               test_desc)]

        proxy = DBProxy()
        db = DBPublisher(proxy)
        db.set_table("test_courses")

        db.publish_courses(test_courses)

        results = proxy.get("SELECT * FROM test_courses")
        print(results)

        proxy.disconnect()
