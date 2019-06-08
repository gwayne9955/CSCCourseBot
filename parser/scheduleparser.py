from typing import *
import requests
from bs4 import BeautifulSoup
from parser.schedulecourse import ScheduleCourse
from parser.coursecode import CourseCode


class ScheduleParser:
    def __init__(self):
        self.SCHEDULE_SOURCE_CUR = "http://schedules.calpoly.edu/depts_52-CENG_curr.htm"
        self.SCHEDULE_SOURCE_NEXT = "http://schedules.calpoly.edu/depts_52-CENG_next.htm"

    def parse_schedule(self) -> Tuple[Dict[int, List[Tuple[str, str]]],
                                      Dict[int, List[Tuple[str, str]]]]:
        cur_quarter = self.invert(self.get_courses(self.SCHEDULE_SOURCE_CUR))
        next_quarter = self.invert(self.get_courses(self.SCHEDULE_SOURCE_NEXT))
        return cur_quarter, next_quarter

    @staticmethod
    def invert(courses: List[ScheduleCourse]) -> \
            Dict[int, List[Tuple[str, str]]]:
        """
        Converts list of (code, professor, time) to inverted index to quickly
        query information about a given class.

        :param courses: List of ScheduleCourses containing course code,
                        professor, and time
        :return course_dict: Inverted index dictionary of
                             Dict[course code: List[(professor, time)]]
        """
        course_dict = {}
        for course in courses:
            try:
                course_dict[course.code.number] \
                    .append((course.prof_name, course.time))
            except KeyError:
                course_dict[course.code.number] = [(course.prof_name, course.time)]
        return course_dict

    @staticmethod
    def get_courses(source: str) -> List[ScheduleCourse]:
        """
        Parses schedules.calpoly.edu to retrieve course schedule information.

        :param source: URL to parse
        :return courses: List of ScheduleCourses containing course code,
                         professor, and time
        """
        request = requests.get(source)
        soup = BeautifulSoup(request.text, "html.parser")
        courses = []
        cur_prof = None
        for i, entry in enumerate(soup.find_all('tr')):
            prof = entry.find('td', attrs={'class': 'personName'})
            if prof is not None:
                name = prof.get_text().split(',')
                cur_prof = name[1].strip() + ' ' + name[0]
                print("Starting {}'s course list".format(cur_prof))
            course = entry.find('td', attrs={'class': 'courseName active'})
            course_type = entry.find('td', attrs={'class': 'courseType'})
            course_days = entry.find('td', attrs={'class': 'courseDays'})
            start_time = entry.find('td', attrs={'class': 'startTime'})
            end_time = entry.find('td', attrs={'class': 'endTime'})
            if course_type is not None and course_type.get_text() == "Lec":
                course = course.get_text().split(' ')
                dept = course[0]
                if (dept == "CPE" or dept == "CSC") and course[1].isdigit():
                    course_code = CourseCode(dept, int(course[1]))

                    time = course_days.get_text() + ' ' + \
                           start_time.get_text() + '-' + \
                           end_time.get_text()

                    schedule_course = ScheduleCourse(course_code, time, cur_prof)
                    courses.append(schedule_course)
                    #print("Course for entry {}: {}".format(i, schedule_course))
        return courses


if __name__ == "__main__":
    parser = ScheduleParser()
    cur, following = parser.parse_schedule()
    print(cur)
