from intent_handling.signal import Signal


class IsClassInTermIntent:
    NAME = 'IS_CLASS_IN_TERM'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        sql = 'SELECT term ' \
              'FROM main_courses JOIN course_terms ON main_courses.code=course_terms.code ' \
              'WHERE main_courses.name="{}"'.format(self.parameters.class_name)
        result = db.call(sql)
        if len(result) == 0:
            return Signal.UNKNOWN, 'No course term information for {} is available.'.format(self.parameters.class_name)
        quarters = ', '.join(result)
        return Signal.NORMAL, '{} is offered in {}.'.format(self.parameters.class_name, quarters)