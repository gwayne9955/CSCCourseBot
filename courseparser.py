import requests
from bs4 import BeautifulSoup
from course import Course
from unitrange import UnitRange

COURSES_SOURCE = "http://catalog.calpoly.edu/coursesaz/csc/"


def get_courses():
    request = requests.get(COURSES_SOURCE)
    soup = BeautifulSoup(request.text, "html.parser")
    courses = []

    course_blocks = soup.find_all('div', attrs={'class': 'courseblock'})
    for course_block in course_blocks:
        full_name, unit_string = tuple(s.strip() for s in course_block.p.strong.strings)
        code, name = tuple(s.strip() for s in full_name.split('.')[:2])
        units = parse_unit_range(unit_string)
        print(code, name, units)
        courses.append(Course(code, name, units))

    return courses


def parse_unit_range(string):
    bounds = [int(s) for s in string.replace('-', ' ').split() if s.isdigit()]
    if len(bounds) == 1:
        return UnitRange.always(bounds[0])
    else:
        return UnitRange(bounds[0], bounds[1])


if __name__ == '__main__':
    get_courses()



