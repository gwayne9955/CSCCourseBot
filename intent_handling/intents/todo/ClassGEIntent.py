from intent_handling.signal import Signal


class ClassGEIntent:
    NAME = 'CLASS_GE_X'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        code = db.
        sql = 'SELECT ge_area ' \
              'FROM course_ge ' \
              'WHERE code="{}"'.format(code)
        result = db.call(sql)
        courses = [row[0] for row in result]
        if self.parameters.class_name not in courses:
            output = 'No, {} does not satisfy GE Area {}.'.format(
                    self.parameters.class_name, self.parameters.ge_area)
            if len()
            output += ' But'
            return Signal.UNKNOWN,

