from intent_handling.intents.LevelClassesInTermIntent import LevelClassesInTermIntent


class TermAnyLevelIntent:
    NAME = 'TERM_ANY_LEVEL_CLASSES'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        return LevelClassesInTermIntent(self.parameters).execute(db)
