import requests
import re
from bs4 import BeautifulSoup
from parser.course import Course
from parser.coursecode import CourseCode
from parser.unitrange import UnitRange
from parser.term import Term


class CourseParser:
    def __init__(self):
        self.COURSES_SOURCE = "http://catalog.calpoly.edu/coursesaz/csc/"
        self.TERM_OFFERING_PREFIX = 'Term Typically Offered: '
        self.PREREQ_PREFIX = 'Prerequisite: '
        self.CR_NC_MARKER = 'CR/NC'
        self.CROSSLIST_REGEX = r'Crosslisted as (\w+/\w+)'

    def get_courses(self):
        request = requests.get(self.COURSES_SOURCE)
        soup = BeautifulSoup(request.text, "html.parser")
        courses = []
    
        course_blocks = soup.find_all('div', attrs={'class': 'courseblock'})
        for course_block in course_blocks:
            full_name, unit_string = tuple(s.strip() for s in course_block.p.strong.strings)
            full_code, name = tuple(s.strip() for s in full_name.split('.')[:2])
            dept, code = tuple(full_code.split())
            code = int(code)
            units = self.parse_unit_range(unit_string)
    
            subheader = course_block.find('div', attrs={'class': 'noindent courseextendedwrap'})
            terms_string = [p.string for p in subheader.find_all('p', attrs={'class': 'noindent'})
                            if p.string.startswith(self.TERM_OFFERING_PREFIX)][0]
            terms = [Term.from_str(t) for t in terms_string[len(self.TERM_OFFERING_PREFIX):].split(', ')]
    
            subheaders = list(subheader.strings)
            is_CRNC = self.CR_NC_MARKER in subheaders
    
            prereq_idx = [idx for idx, string in enumerate(subheaders) if string.startswith(self.PREREQ_PREFIX)]
            if len(prereq_idx) == 0:
                prereqs = None
            else:
                prereqs = ''.join(subheaders[prereq_idx[0]:])[len(self.PREREQ_PREFIX):]
    
            desc = ''.join(course_block.find('div', attrs={'class': 'courseblockdesc'}).p.strings)
            crosslist = re.search(self.CROSSLIST_REGEX, desc)
            if crosslist:
               dept = crosslist.group(1)
    
            course = Course(CourseCode(dept, code), name, units,
                            terms, is_CRNC, prereqs, desc)
            courses.append(course)
    
        return courses
    
    @staticmethod
    def parse_unit_range(string):
        bounds = [int(s) for s in string.replace('-', ' ').split() if s.isdigit()]
        if len(bounds) == 1:
            return UnitRange.always(bounds[0])
        else:
            return UnitRange(bounds[0], bounds[1])
