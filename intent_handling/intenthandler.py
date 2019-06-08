from typing import *
from intent_handling.intents.IsClassInTermIntent import IsClassInTermIntent
from intent_handling.parameters import Parameters


class IntentHandler:
    ALL_INTENTS: List[type] = [IsClassInTermIntent]

    INTENT_MAPPING: Dict[str, type] = {IntentType.NAME: IntentType
                                       for IntentType in ALL_INTENTS}

    def handle(self, intent_name: str, parameters: Dict) -> str:
        if intent_name not in IntentHandler.INTENT_MAPPING:
            return "Sorry, I'm not sure how to answer that."

        IntentType = IntentHandler.INTENT_MAPPING[intent_name]
        params = Parameters(parameters)
        return IntentType(params).execute()
