from intent_handling.intents.LinkToFlowchart import LinkToFlowchart


class ClassesComplimentClass:
    NAME = 'CLASSES_COMPLIMENT_CLASS'

    def __init__(self, parameters):
        self.parameters = parameters

    @staticmethod
    def execute(db):
        return LinkToFlowchart().execute()
