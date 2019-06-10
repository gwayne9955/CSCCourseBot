from intent_handling.intents.TermsClassOfferedIntent import TermsClassOfferedIntent


class IsClassInTermIntent:
    NAME = 'IS_CLASS_IN_TERM'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        return TermsClassOfferedIntent(self.parameters).execute(db)
