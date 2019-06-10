from intent_handling.signal import Signal


class ClassesOnlyInTermIntent:
    NAME = 'CLASSES_ONLY_IN_TERM'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        sql = 'SELECT * FROM course_terms'
        result = db.call(sql)
        print(result)
