from intent_handling.signal import Signal
from intent_handling.util import *


class ClassesOnlyInTermIntent:
    NAME = 'CLASSES_ONLY_IN_TERM'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        sql = 'SELECT * FROM course_terms'
        result = db.call(sql)
        by_term = assoc(result, key=lambda pair: pair[0], value=lambda pair: pair[1])
        matching = [course for course, terms in by_term.items()
                    if len(terms) == 1 and terms[0] == self.parameters.quarter]
        if len(matching) == 0:
            return Signal.UNKNOWN, 'No course information available for {}.'.format(self.parameters.quarter)
        courses = ', '.join(sorted(matching))
        return Signal.NORMAL, 'The following courses are typically offered only in {}: {}.'.format(self.parameters.quarter, courses)
