from intent_handling.signal import Signal


class PrereqsForClassIntent:
    NAME = 'CLASS_WHAT_PREREQS'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        sql = 'SELECT prereqs from main_courses WHERE intent_name="{}"'.format(self.parameters.class_name)
        result = db.call(sql)
        if len(result) == 0:
            return Signal.UNKNOWN, 'No prerequisite information available for {}'.format(self.parameters.class_name)
        prereqs = result[0][0]
        code = db.course_code(self.parameters.class_name)
        if prereqs == '':
            return Signal.NORMAL, '{} has no prerequisites.'.format(code)
        return Signal.NORMAL, 'The prerequisites for {} are: {}'.format(code, prereqs)
