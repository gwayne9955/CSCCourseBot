from intent_handling.signal import Signal


class ClassesGEIntent:
    NAME = 'CLASSES_GE_X'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        sql = 'SELECT code ' \
              'FROM course_ge ' \
              'WHERE ge_area="{}"'.format(self.parameters.ge_area.lower())
        result = db.call(sql)

        if len(result) == 0:
            output = 'No CSC classes found to fulfill GE Area {}'.format(
                self.parameters.ge_area)
            return Signal.UNKNOWN, output

        codes = [row[0] for row in result]
        output = 'The following classes fulfill GE Area {}\n'.format(
            self.parameters.ge_area)
        for code in codes:
            output += '\tCSC {}\n'.format(code)

        return Signal.NORMAL, output
