import os
import sys
from storage.DBProxy import DBProxy
from storage.DBPublisher import DBPublisher
from parser.courseparser import CourseParser

cur_path = os.getcwd()
sys.path.insert(0, '/'.join(cur_path.split('/')[:-1]))


def main():
    proxy = DBProxy()
    db = DBPublisher(proxy)
    parser = CourseParser()

    db.cleanup()

    catalog = parser.get_courses()
    db.publish_catalog(catalog)

    proxy.disconnect()


if __name__ == "__main__":
    main()
