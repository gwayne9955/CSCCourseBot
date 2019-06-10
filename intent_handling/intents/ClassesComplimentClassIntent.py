from intent_handling.intents.LinkToFlowchartIntent import LinkToFlowchart


class ClassesComplimentClassIntent:
    NAME = 'CLASSES_COMPLIMENT_CLASS'

    def __init__(self, parameters):
        self.parameters = parameters

    @staticmethod
    def execute(db):
        output = 'The CSC flowchart would be best to see what classes ' \
                 'compliment each other. '
        return output + LinkToFlowchart().execute()
