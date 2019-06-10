from intent_handling.signal import Signal


class ClassHasLabIntent:
    NAME = 'CLASSES_LAB'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        sql = 'SELECT description ' \
              'FROM main_courses ' \
              'WHERE intent_name="{}"'.format(self.parameters.class_name)
        result = db.call(sql)
        if len(result) == 0:
            return Signal.UNKNOWN, 'No information about {} is available.'.format(self.parameters.class_name)
        code = db.class_code(self.parameters.class_name)
        description = result[0][0]
        if 'laboratory' in description:
            return Signal.NORMAL, 'Yes, {} has a lab section.'.format(code)
        else:
            return Signal.NORMAL, 'No, {} does not have a lab section.'.format(code)
