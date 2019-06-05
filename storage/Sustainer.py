import os
import sys
cur_path = os.getcwd()
sys.path.insert(0, '/'.join(cur_path.split('/')[:-1]))

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
