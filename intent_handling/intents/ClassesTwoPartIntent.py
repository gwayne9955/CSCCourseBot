from intent_handling.intents.LinkToFlowchartIntent import LinkToFlowchart


class ClassesTwoPartIntent:
    NAME = 'CLASSES_TWO_PART'

    def __init__(self, parameters):
        self.parameters = parameters

    @staticmethod
    def execute(db):
        return LinkToFlowchart().execute()
