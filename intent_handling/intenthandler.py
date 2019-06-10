from typing import *
from storage.DBProxy import DBProxy
from intent_handling.intents.TermsClassOfferedIntent import TermsClassOfferedIntent
from intent_handling.intents.ClassesComplimentClassIntent import ClassesComplimentClass
from intent_handling.intents.ClassesWithTopicIntent import ClassesWithTopicIntent
from intent_handling.intents.ClassGEIntent import ClassGEIntent
from intent_handling.parameters import Parameters


class IntentHandler:
    ALL_INTENTS: List[type] = [TermsClassOfferedIntent,
                               ClassesComplimentClass,
                               ClassesWithTopicIntent,
                               ClassGEIntent]

    INTENT_MAPPING: Dict[str, type] = {IntentType.NAME: IntentType
                                       for IntentType in ALL_INTENTS}

    def __init__(self, db: DBProxy):
        self.db = db

    def handle(self, intent_name: str, parameters: Dict) -> str:
        if intent_name not in IntentHandler.INTENT_MAPPING:
            return "Sorry, I'm not sure how to answer that."

        IntentType = IntentHandler.INTENT_MAPPING[intent_name]
        params = Parameters(parameters)
        response = IntentType(params).execute(self.db)
        return response
