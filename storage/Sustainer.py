import sys
sys.path.insert(0, "/home/silveria466/CSCCourseBot")

from storage.DBProxy import DBProxy
from storage.DBPublisher import DBPublisher
from parser.courseparser import CourseParser


def main():
    proxy = DBProxy()
    db = DBPublisher(proxy)
    parser = CourseParser()

    db.cleanup()

    courses = parser.get_courses()
    db.publish_courses(courses)

    proxy.disconnect()


if __name__ == "__main__":
    main()
