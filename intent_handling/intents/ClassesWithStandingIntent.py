from intent_handling.signal import Signal


class ClassesWithStandingIntent:
    NAME = 'CLASSES_REQ_STANDING'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        sql = 'SELECT code, prereqs FROM main_courses'
        result = db.call(sql)
        matching = ['CSC {}'.format(c) for c, prereqs in result
                    if '{} standing'.format(self.parameters.class_qualification) in prereqs.lower()]
        if len(matching) == 0:
            return Signal.NORMAL, 'No classes require {} standing.'.format(self.parameters.class_qualification)
        return Signal.NORMAL, 'The following classes require {} standing: {}.'.format(
            self.parameters.class_qualification, ', '.join(matching))