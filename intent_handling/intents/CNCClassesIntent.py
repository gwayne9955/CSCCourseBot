from intent_handling.signal import Signal


class CNCClassesIntent:
    NAME = 'CLASSES_CNC'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        sql = 'SELECT code FROM main_courses WHERE is_crnc=1'
        result = db.call(sql)
        crnc = ', '.join('CSC {}'.format(tup[0]) for tup in result)
        return Signal.NORMAL, 'The following classes are credit/no credit grading only: {}.'.format(crnc)
