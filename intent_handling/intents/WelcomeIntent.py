from intent_handling.signal import Signal


class WelcomeIntent:
    NAME = 'Default Welcome Intent'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        return Signal.NORMAL, 'Why hello there!'
