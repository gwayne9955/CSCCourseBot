from intent_handling.signal import Signal


class ClassGEIntent:
    NAME = 'CLASS_GE_X'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        code = db.course_code(self.parameters.class_name)
        sql = 'SELECT ge_area ' \
              'FROM course_ge ' \
              'WHERE code="{}"'.format(code.split(' ')[-1])
        result = db.call(sql)
        print("Result from selecting GE Area for {}: {}".format(code, result))
        ge_areas = [row[0] for row in result]
        satisfied = ', '.join([ge.upper() for ge in ge_areas])
        if self.parameters.ge_area.lower() not in ge_areas:
            output = 'No, {} does not satisfy GE Area {}.'.format(
                    code, self.parameters.ge_area)
            if len(ge_areas) > 0:
                output += ' But, {} does satisfy GE Areas {}'.format(
                    self.parameters.class_name, satisfied)
            return Signal.UNKNOWN, output

        output = 'Yes, {} satisfies the following GE Areas {}'.format(
            code, satisfied)
        return Signal.NORMAL, output

