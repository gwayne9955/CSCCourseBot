from intent_handling.signal import Signal
from intent_handling.util import *


class ClassesCrosslistedIntent:
    NAME = 'CLASSES_CROSSLISTED'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        dept = self.parameters.department_abbreviation
        sql = 'SELECT code ' \
              'FROM course_depts ' \
              'WHERE department="{}"'.format(dept.lower())
        result = db.call(sql)
        if len(result) == 0:
            return Signal.NORMAL, 'No classes are crosslisted in {}.'.format(dept)
        matching = ', '.join('CSC {}'.format(tup[0]) for tup in result)
        return Signal.NORMAL, 'The following classes are crosslisted in {}: {}.'.format(dept, matching)
