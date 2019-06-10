from intent_handling.intents.PrereqsForClassIntent import PrereqsForClassIntent


class ClassRequiresStandingIntent:
    NAME = 'CLASS_REQ_STANDING'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        return PrereqsForClassIntent(self.parameters).execute(db)
