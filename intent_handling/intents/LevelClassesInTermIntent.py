from intent_handling.signal import Signal


class LevelClassesInTermIntent:
    NAME = 'LEVEL_CLASSES_IN_TERM'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        sql = 'SELECT code FROM course_terms ' \
              'WHERE code >= {} AND code <= {} AND term="{}"'.format(
            self.parameters.course_level,
            self.parameters.course_level + 100,
            self.parameters.quarter
        )
        result = db.call(sql)
        if len(result) == 0:
            return Signal.UNKNOWN, 'No {} level course data available for {}.'.format(
                self.parameters.course_level,
                self.parameters.quarter
            )
        courses = ', '.join('CSC {}'.format(tup[0]) for tup in result)
        return Signal.NORMAL, 'The following {} level courses are offered in {}: {}.'.format(
            self.parameters.course_level,
            self.parameters.quarter,
            courses
        )
