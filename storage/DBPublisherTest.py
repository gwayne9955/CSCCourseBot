import os
import sys
cur_path = os.getcwd()
sys.path.insert(0, '/'.join(cur_path.split('/')[:-1]))

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
        test_course_code = CourseCode("CSC/CPE", 466)
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
                    "1 laboratory.  "

        test_courses = [Course(test_course_code,
                               test_couse_name,
                               test_unit_range,
                               test_terms,
                               test_iscrnc,
                               test_prereqs,
                               test_desc)]

        proxy = DBProxy()
        db = DBPublisher(proxy)
        db.set_table_prefix("test")

        db.publish_courses(test_courses)

        #results = proxy.get("SELECT * FROM test_courses")
        #print(results)
        cleanup = input("Cleanup test tables? (y/n): ")
        if (cleanup == "y"):
            proxy.truncate("test_main_courses")
            proxy.truncate("test_course_terms")
            proxy.truncate("test_course_depts")

        proxy.disconnect()


if __name__ == "__main__":
   unittest.main()
