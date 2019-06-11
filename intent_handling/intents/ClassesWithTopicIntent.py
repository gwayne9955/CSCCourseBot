from intent_handling.signal import Signal


class ClassesWithTopicIntent:
    NAME = 'CLASSES_WITH_TOPIC'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        pretty_topic = ' '.join(self.parameters.subject_matter.split('_'))
        sql = 'SELECT code ' \
              'FROM course_topics ' \
              'WHERE topic="{}"'.format(self.parameters.subject_matter)
        result = db.call(sql)
        if len(result) == 0:
            return Signal.UNKNOWN, 'No classes found with topic {}'.format(
                pretty_topic)

        codes = [row[0] for row in result]
        output = "The following classes are related to {}: {}".format(
            pretty_topic, ', '.join(["CSC {}".format(c) for c in codes]))

        return Signal.NORMAL, output

