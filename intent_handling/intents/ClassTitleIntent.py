from intent_handling.signal import Signal


class ClassTitleIntent:
    NAME = 'CLASS_TITLE'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        code = db.course_code(self.parameters.class_name)
        sql = 'SELECT pretty_name ' \
              'FROM main_courses ' \
              'WHERE code="{}"'.format(code)
        result = db.call(sql)

        output = "CSC {}'s course name is {}".format(code, result[0][0])

        return Signal.NORMAL, output
