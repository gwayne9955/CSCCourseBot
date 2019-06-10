from intent_handling.signal import Signal


class ClassesInTermIntent:
    NAME = 'WHAT_CLASSES_IN_TERM'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        sql = 'SELECT main_courses.code ' \
              'FROM main_courses JOIN course_terms ON main_courses.code=course_terms.code ' \
              'WHERE term="{}"'.format(self.parameters.quarter)
        result = db.call(sql)
        if len(result) == 0:
            return Signal.UNKNOWN, 'No term information for {} is available.'.format(
                self.parameters.quarter)

        courses = ', '.join('CSC {}'.format(tup[0]) for tup in result)
        return Signal.NORMAL, 'The following courses are offered in {}: {}.'.format(self.parameters.quarter, courses)
