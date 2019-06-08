import os
import sys
from storage.DBProxy import DBProxy
from storage.DBPublisher import DBPublisher
from parser.courseparser import CourseParser
from parser.scheduleparser import ScheduleParser

cur_path = os.getcwd()
sys.path.insert(0, '/'.join(cur_path.split('/')[:-1]))


def main():
    proxy = DBProxy()
    db = DBPublisher(proxy)
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
