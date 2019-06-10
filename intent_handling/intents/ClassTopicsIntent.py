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
        topics = topics[:10]
        output = "Here are {} topics are covered in {}:\n".format(
            len(topics), code)
        for topic in topics:
            pretty_topic = ' '.join(topic.split('_'))
            output += '\t{}\n'.format(pretty_topic)

        return Signal.NORMAL, output

