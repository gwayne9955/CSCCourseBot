from typing import *
from storage.DBProxy import DBProxy
from intent_handling.intents.ClassesInTermIntent import ClassesInTermIntent
from intent_handling.intents.ClassesOnlyInTermIntent import ClassesOnlyInTermIntent
from intent_handling.intents.ClassesWithPrerequisiteIntent import ClassesWithPrerequisiteIntent
from intent_handling.intents.ClassesWithStandingIntent import ClassesWithStandingIntent
from intent_handling.intents.IsClassInTermIntent import IsClassInTermIntent
from intent_handling.intents.LevelClassesInTermIntent import LevelClassesInTermIntent
from intent_handling.intents.PrereqsForClassIntent import PrereqsForClassIntent
from intent_handling.intents.TermAllLowerIntent import TermAllLowerIntent
from intent_handling.intents.TermAllUpperIntent import TermAllUpperIntent
from intent_handling.intents.TermAnyLevelIntent import TermAnyLevelIntent
from intent_handling.intents.TermsClassOfferedIntent import TermsClassOfferedIntent
from intent_handling.intents.ClassesComplimentClassIntent import ClassesComplimentClassIntent
from intent_handling.intents.ClassesWithTopicIntent import ClassesWithTopicIntent
from intent_handling.intents.ClassGEIntent import ClassGEIntent
from intent_handling.intents.ClassesGEIntent import ClassesGEIntent
from intent_handling.intents.ClassesTwoPartIntent import ClassesTwoPartIntent
from intent_handling.intents.ClassAfterClassIntent import ClassAfterClassIntent
from intent_handling.intents.WhatClassCodeIntent import WhatClassCodeIntent
from intent_handling.intents.ClassTitleIntent import ClassTitleIntent

from intent_handling.intents.ClassCrosslistedIntent import ClassCrosslistedIntent
from intent_handling.intents.ClassesCrosslistedIntent import ClassesCrosslistedIntent
from intent_handling.intents.ClassCrosslistedInDeptIntent import ClassCrosslistedInDeptIntent
from intent_handling.intents.ClassesCrosslistedInDeptIntent import ClassesCrosslistedInDeptIntent
from intent_handling.intents.ClassHasLabIntent import ClassHasLabIntent
from intent_handling.intents.ClassIsUnitsIntent import ClassIsUnitsIntent
from intent_handling.intents.ClassesNumUnitsIntent import ClassesNumUnitsIntent
from intent_handling.intents.CNCClassesIntent import CNCClassesIntent
from intent_handling.intents.WhenTakeClassIntent import WhenTakeClassIntent
from intent_handling.intents.SeminarClassesIntent import SeminarClassesIntent
from intent_handling.intents.UnitCountIntent import UnitCountIntent
from intent_handling.parameters import Parameters


class IntentHandler:
    ALL_INTENTS: List[type] = [
        ClassesInTermIntent, ClassesOnlyInTermIntent, ClassesWithPrerequisiteIntent,
        ClassesWithStandingIntent, IsClassInTermIntent, ClassHasLabIntent,
        LevelClassesInTermIntent, PrereqsForClassIntent, TermAllLowerIntent,
        TermAllUpperIntent, TermAnyLevelIntent, UnitCountIntent, WhenTakeClassIntent,
        ClassesNumUnitsIntent, ClassIsUnitsIntent, ClassesCrosslistedIntent,
        ClassCrosslistedIntent, ClassCrosslistedInDeptIntent, ClassesCrosslistedInDeptIntent,
        SeminarClassesIntent, CNCClassesIntent,
        TermsClassOfferedIntent,
        TermsClassOfferedIntent,
        ClassesComplimentClassIntent,
        ClassesWithTopicIntent,
        ClassGEIntent,
        ClassesGEIntent,
        ClassesTwoPartIntent,
        ClassAfterClassIntent,
        WhatClassCodeIntent,
        ClassTitleIntent
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
