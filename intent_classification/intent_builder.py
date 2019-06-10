import json
import uuid
import sample
import sys

sample_map = json.load(open('sample_map.json', 'r'))
entity_map = json.load(open('entity_map.json', 'r'))

class Intent():
    def __init__(self, name, sample_frame):
        self.id = str(uuid.uuid4())
        self.name = name
        self.sample_frame = sample_frame
        self.frame = None
        self.phrases = []
        self.build()
        self.build_phrases(sample_frame)

    def build(self):
        self.frame = {
            "id": self.id,
            "name": self.name,
            "displayName": self.name,
            "action": "CSC_BOT",
            "responses": [
                {
                    "resetContexts": False,
                    "affectedContexts": [],
                    "parameters": [],
                    "messages": [
                        {
                            "type": 0,
                            "lang": "en",
                            "speech": []
                        }
                    ],
                    "defaultResponsePlatforms": {},
                    "speech": []
                }
            ]
        }
        self.build_parameters()

    def build_phrases(self, sample_frame):
        phrases = sample_map[sample_frame]['rephrases']
        phrases.append(key)
        samples = []
        vals_per_question = 10
        for phrase in phrases:
            for i in range(vals_per_question):
                s = sample.Sample(phrase, self.name)
                s.populate_entities(entity_map)
                samples.append(s)

        for s in samples:
            self.build_phrase(s)

    def build_phrase(self, s):
        phrase = {
          "id": str(uuid.uuid4()),
          "data": [],
          "isTemplate": False,
          "count": 0
        }
        text_len = len(s.text)
        index = 0
        # go through each entity and add phrase part to data
        for entity in s.entities:
            if entity['start'] > index:
                phrase['data'].append({
                    "text": s.text[index:entity['start']],
                    "userDefined": False
                })
                index += len(s.text[index:entity['start']])

            # if number, use sys.number class
            if entity['entity'] == 'NUMBER':
                phrase['data'].append({
                    "text": entity['value'],
                    "userDefined": False,
                    "alias": "number",
                    "meta": "@sys.number"
                })
            else: # not number, use defined entity type
                phrase['data'].append({
                    "text": entity['value'],
                    "userDefined": False,
                    "alias": entity['entity'],
                    "meta": "@{}".format(entity['entity'])
                })
            index += len(entity['value'])
        # add remaining string
        if index < len(s.text):
            phrase['data'].append({
                "text": s.text[index:],
                "userDefined": False
            })
        self.phrases.append(phrase)

    def build_parameters(self):
        """Build the parameters for this intent"""
        for key in entity_map:
            if key in self.sample_frame:
                parameter = {
                    "id": str(uuid.uuid4()),
                    "required": True,
                    "name": entity_map[key]['entity_type'],
                    "dataType": "@{}".format(entity_map[key]['entity_type']),
                    "value": "${}".format(entity_map[key]['entity_type']),
                    "isList": False
                }
                self.frame['responses'][0]['parameters'].append(parameter)

    def write_to_file(self):
        with open("./CSC466Bot/intents/{}.json".format(self.name), 'w+') as f_out:
            json.dump(self.frame, f_out)
        with open("./CSC466Bot/intents/{}_usersays_en.json".format(self.name), 'w+') as f_phrases_out:
            json.dump(self.phrases, f_phrases_out)

if __name__ == '__main__':
    for key in sample_map:
        intent_name = sample_map[key]['intent']
        intent = Intent(intent_name, key)
        intent.write_to_file()
