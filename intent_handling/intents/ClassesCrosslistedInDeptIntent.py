from intent_handling.intents.ClassesCrosslistedIntent import ClassesCrosslistedIntent


class ClassesCrosslistedInDeptIntent:
    NAME = 'CLASSES_CROSSLISTED_DEP'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        return ClassesCrosslistedIntent(self.parameters).execute(db)
