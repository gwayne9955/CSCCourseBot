from typing import *
from storage.DBProxy import DBProxy
from intent_handling.intents.ClassesInTermIntent import ClassesInTermIntent
from intent_handling.intents.ClassesOnlyInTermIntent import ClassesOnlyInTermIntent
from intent_handling.intents.ClassesWithPrerequisiteIntent import ClassesWithPrerequisiteIntent
from intent_handling.intents.IsClassInTermIntent import IsClassInTermIntent
from intent_handling.intents.LevelClassesInTermIntent import LevelClassesInTermIntent
from intent_handling.intents.PrereqsForClassIntent import PrereqsForClassIntent
from intent_handling.intents.TermAllLowerIntent import TermAllLowerIntent
from intent_handling.intents.TermAllUpperIntent import TermAllUpperIntent
from intent_handling.intents.TermAnyLevelIntent import TermAnyLevelIntent
from intent_handling.intents.TermsClassOfferedIntent import TermsClassOfferedIntent
from intent_handling.parameters import Parameters


class IntentHandler:
    ALL_INTENTS: List[type] = [
        ClassesInTermIntent, ClassesOnlyInTermIntent, ClassesWithPrerequisiteIntent,
        IsClassInTermIntent,
        LevelClassesInTermIntent, PrereqsForClassIntent, TermAllLowerIntent,
        TermAllUpperIntent, TermAnyLevelIntent,
        TermsClassOfferedIntent,
    ]

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
