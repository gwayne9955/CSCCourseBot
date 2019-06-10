from intent_handling.signal import Signal


class ClassesWithTopicIntent:
    NAME = 'CLASSES_WITH_TOPIC'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        sql = 'SELECT code ' \
              'FROM course_topics ' \
              'WHERE topic="{}"'.format(self.parameters.subject_matter)
        result = db.call(sql)
        if len(result) == 0:
            return Signal.UNKNOWN, 'No classes found with topic {}'.format(
                self.parameters.subject_matter)

        output = "The following classes are related to {}:\n\n".format(
            self.parameters.subject_matter)
        for course in result:
            output += "\tCSC {}\n".format(course[0])

        return Signal.NORMAL, output

