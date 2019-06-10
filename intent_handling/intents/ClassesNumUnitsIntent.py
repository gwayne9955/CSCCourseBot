from intent_handling.signal import Signal


class ClassesNumUnitsIntent:
    NAME = 'CLASSES_X_UNITS'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        sql = 'SELECT code ' \
              'FROM main_courses ' \
              'WHERE min_units={} AND max_units={}'.format(self.parameters.number, self.parameters.number)
        result = db.call(sql)
        if len(result) == 0:
            return Signal.NORMAL, 'No classes are {} units.'.format(self.parameters.number)
        matching = ', '.join('CSC {}'.format(code) for code in result)
        return Signal.NORMAL, 'The following classes are {} units: {}.'.format(self.parameters.number, matching)
