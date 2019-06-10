from intent_handling.signal import Signal


class SeminarClassesIntent:
    NAME = 'CLASSES_SEMINAR'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        sql = 'SELECT code, description FROM main_courses'
        result = db.call(sql)
        matching = ', '.join('CSC {}'.format(code) for code, desc in result
                             if 'seminar' in desc)
        return Signal.NORMAL, 'The following classes are seminars: {}.'.format(matching)
