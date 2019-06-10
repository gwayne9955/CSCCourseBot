from intent_handling.signal import Signal


class ClassesWithPrerequisiteIntent:
    NAME = 'WHICH_CLASSES_REQUIRE_CLASS'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        sql = 'SELECT code, prereqs FROM main_courses'
        result = db.call(sql)
        code = db.call('SELECT code FROM main_courses WHERE intent_name="{}"'.format(self.parameters.class_name))
        matching = ['CSC {}'.format(c) for c, prereqs in result
                    if 'CSC {}'.format(code) in prereqs
                    or 'CSC/CPE {}'.format(code) in prereqs]
        if len(matching) == 0:
            return Signal.NORMAL, 'No classes require CSC {}.'.format(code)
        return Signal.NORMAL, 'The following classes require CSC {}: {}.'.format(code, ', '.join(matching))
