from intent_handling.signal import Signal


class ClassCNCIntent:
    NAME = 'CLASS_CNC'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        code = db.course_code(self.parameters.class_name)
        sql = 'SELECT is_crnc ' \
              'FROM main_courses ' \
              'WHERE code="{}"'.format(code.split(' ')[-1])
        result = db.call(sql)

        is_crnc = result[0][0]
        if is_crnc == 1:
            output = 'Yes, {} is credit/no credit grading only.'.format(code)
        else:
            output = 'No, {} is not credit/no credit grading only.'.format(code)

        return Signal.NORMAL, output

