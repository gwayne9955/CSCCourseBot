from intent_handling.signal import Signal
from intent_handling.util import *


class ClassesCrosslistedIntent:
    NAME = 'CLASSES_CROSSLISTED'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        sql = 'SELECT code, department FROM course_depts'
        result = db.call(sql)
        by_code = assoc(result,
                        key=lambda pair: pair[0],
                        value=lambda pair: pair[1])
        by_code = {code: '/'.join(sorted(dept.upper() for dept in depts))
                   for code, depts in by_code.items()
                   if len(depts) > 1}
        crosslisted = ', '.join('{} {}'.format(by_code[code], code)
                                for code in sorted(by_code))
        return Signal.NORMAL, 'The following courses are crosslisted: {}.'.format(crosslisted)
