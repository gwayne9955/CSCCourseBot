from intent_handling.signal import Signal


class ClassCrosslistedIntent:
    NAME = 'CLASS_CROSSLISTED'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        sql = 'SELECT code, department ' \
              'FROM course_depts JOIN main_courses ON course_depts.code=main_courses.code ' \
              'WHERE intent_name="{}"'.format(self.parameters.class_name)
        result = db.call(sql)
        if len(result) == 0:
            return Signal.UNKNOWN, 'No information available for {}.'.format(self.parameters.class_name)
        else:
            code_string = db.course_code(self.parameters.class_name)
            if len(result) == 1:
                return Signal.NORMAL, '{} is not crosslisted in any other departments.'.format(code_string)
            else:
                crosslisted = ', '.join('{} {}'.format(tup[1].upper(), tup[0]) for tup in result)
                return Signal.NORMAL, '{} is crosslisted as {}.'.format(code_string, crosslisted)
