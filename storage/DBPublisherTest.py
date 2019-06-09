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
from storage.preprocessor import Preprocessor
from storage.DBPublisher import DBPublisher


class TestDBPublisher(unittest.TestCase):

    def setUp(self) -> None:
        self.proxy = DBProxy()
        self.preprocessor = Preprocessor()
        self.db = DBPublisher(self.proxy, self.preprocessor)
        self.db.set_table_prefix("test_")

    def tearDown(self) -> None:
        self.proxy.disconnect()

    # Wet run test, will add to database on Frank
    def test_publish_catalog(self):
        self.db.cleanup()

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

        self.db.publish_catalog(test_courses)

    def test_publish_schedule(self):
        cur_schedule = {466: [("Foaad Khosmood", "TR 12:10 AM-1:30 PM")],
                        471: [("Zoe J. Wood", "TR 8:10 AM-9:30AM")]}
        next_schedule = {482: [("Foaad Khosmood", "TR 8:10 AM-9:30 PM")],
                         466: [("Foaad Khosmood", "TR 12:10 AM-1:30 PM"),
                               ("Foaad Khosmood", "MWF 10:10 AM-11:00 AM")]}

        self.db.publish_schedule((cur_schedule, next_schedule))


if __name__ == "__main__":
    unittest.main()
