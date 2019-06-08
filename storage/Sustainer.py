import os
import sys
cur_path = os.getcwd()
sys.path.insert(0, '/'.join(cur_path.split('/')[:-1]))

from storage.DBProxy import DBProxy
from storage.DBPublisher import DBPublisher
from storage.preprocessor import Preprocessor
from parser.courseparser import CourseParser
from parser.scheduleparser import ScheduleParser


def main():
    proxy = DBProxy()
    preprocessor = Preprocessor()
    db = DBPublisher(proxy, preprocessor)
    course_parser = CourseParser()
    schedule_parser = ScheduleParser()

    db.cleanup()

    catalog = course_parser.get_courses()
    db.publish_catalog(catalog)

    cur_quarter, next_quarter = schedule_parser.parse_schedule()
    db.publish_schedule((cur_quarter, next_quarter))

    proxy.disconnect()


if __name__ == "__main__":
    main()
