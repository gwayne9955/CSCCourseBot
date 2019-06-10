from intent_handling.intents.LinkToFlowchartIntent import LinkToFlowchart


class ClassAfterClassIntent:
    NAME = 'CLASS_AFTER_CLASS'

    def __init__(self, parameters):
        self.parameters = parameters

    @staticmethod
    def execute(db):
        output = "The CSC flowchart would be best to understand what order to" \
                 " take courses. "
        flowchart = LinkToFlowchart().execute()
        return flowchart[0], output + flowchart[1]
