from intent_handling.signal import Signal


class TermAllLowerIntent:
    NAME = 'TERM_ALL_LOWER'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        sql = 'SELECT code from course_terms WHERE code < 300 AND term="{}"'.format(
            self.parameters.quarter)
        result = db.call(sql)
        if len(result) == 0:
            return Signal.UNKNOWN, 'No lower division course data available for {}.'.format(
                self.parameters.quarter)
        courses = ', '.join('CSC {}'.format(tup[0]) for tup in result)
        return Signal.NORMAL, 'The following lower division courses are offered in {}: {}.'.format(
            self.parameters.quarter, courses)
