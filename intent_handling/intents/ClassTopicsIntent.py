from intent_handling.signal import Signal


class ClassTopicsIntent:
    NAME = 'CLASS_TOPICS'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        code = db.course_code(self.parameters.class_name)
        sql = 'SELECT topic ' \
              'FROM course_topics ' \
              'WHERE code="{}"'.format(code.split(' ')[-1])
        result = db.call(sql)

        topics = [row[0] for row in result]
        topics = [' '.join(topic.split('_')) for topic in topics[:10]]
        output = "Here are {} topics are covered in {}: {}".format(
            len(topics), code, ', '.join(topics))

        return Signal.NORMAL, output

