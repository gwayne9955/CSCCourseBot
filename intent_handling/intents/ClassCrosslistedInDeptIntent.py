from intent_handling.intents.ClassCrosslistedIntent import ClassCrosslistedIntent


class ClassCrosslistedInDeptIntent:
    NAME = 'CLASS_CROSSLISTED_DEP'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        return ClassCrosslistedIntent(self.parameters).execute(db)
