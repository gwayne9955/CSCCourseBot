from intent_handling.signal import Signal


class ClassWithTopicIntent:
    NAME = 'CLASS_WITH_TOPIC'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        pretty_topic = ' '.join(self.parameters.subject_matter.split('_'))
        code = db.course_code(self.parameters.class_name)
        sql = 'SELECT code ' \
              'FROM course_topics ' \
              'WHERE topic="{}"'.format(self.parameters.subject_matter)
        result = db.call(sql)

        codes = [row[0] for row in result]
        print("Codes: {}, searching for: {}".format(codes, code.split(' ')[-1]))
        if int(code.split(' ')[-1]) not in codes:
            output = 'No, {} does not cover {}.'.format(
                code, pretty_topic)
            if len(codes) > 0:
                output += ' But, {} is covered in the following classes:\n'.format(
                    pretty_topic)
                for c in codes:
                    output += '\tCSC {}\n'.format(c)
            return Signal.UNKNOWN, output

        output = 'Yes, {} covers {}.'.format(code,
                                             pretty_topic)
        if len(codes) > 1:
            output += ' {} is covered in the following classes:\n'.format(
                pretty_topic)
            for c in codes:
                output += '\tCSC {}\n'.format(c)
        return Signal.NORMAL, output
