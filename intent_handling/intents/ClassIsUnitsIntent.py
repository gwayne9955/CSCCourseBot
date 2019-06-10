from intent_handling.intents.UnitCountIntent import UnitCountIntent


class ClassIsUnitsIntent:
    NAME = 'CLASS_X_UNITS'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        return UnitCountIntent(self.parameters).execute(db)
