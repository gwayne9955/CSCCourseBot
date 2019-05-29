import requests
from bs4 import BeautifulSoup
from course import Course
from coursecode import CourseCode
from unitrange import UnitRange
from term import Term

COURSES_SOURCE = "http://catalog.calpoly.edu/coursesaz/csc/"
TERM_OFFERING_PREFIX = 'Term Typically Offered: '


def get_courses():
    request = requests.get(COURSES_SOURCE)
    soup = BeautifulSoup(request.text, "html.parser")
    courses = []

    course_blocks = soup.find_all('div', attrs={'class': 'courseblock'})
    for course_block in course_blocks:
        full_name, unit_string = tuple(s.strip() for s in course_block.p.strong.strings)
        full_code, name = tuple(s.strip() for s in full_name.split('.')[:2])
        dept, code = tuple(full_code.split())
        code = int(code)
        units = parse_unit_range(unit_string)

        subheader = course_block.find('div', attrs={'class': 'noindent courseextendedwrap'})
        terms_string = [p.string for p in subheader.find_all('p', attrs={'class': 'noindent'})
                        if p.string.startswith(TERM_OFFERING_PREFIX)][0]
        terms = [Term.from_str(t) for t in terms_string[len(TERM_OFFERING_PREFIX):].split(', ')]

        course = Course(CourseCode(dept, code), name, units, terms)
        courses.append(course)
        print(course)

    return courses


def parse_unit_range(string):
    bounds = [int(s) for s in string.replace('-', ' ').split() if s.isdigit()]
    if len(bounds) == 1:
        return UnitRange.always(bounds[0])
    else:
        return UnitRange(bounds[0], bounds[1])


if __name__ == '__main__':
    get_courses()



