from intent_handling.intents.LinkToFlowchartIntent import LinkToFlowchart


class WhenTakeClassIntent:
    NAME = 'WHEN_MOST_TAKE_CLASS'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        return LinkToFlowchart.execute()
