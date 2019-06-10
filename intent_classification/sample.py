import random
import re


# find all occurances of a string in another
def find_all(str, sub):
    """Method to find all occurances of a string in another
    Args:
        str (str): a string to search within
        sub (str): a substring to search for
    Return:
        List of integers representing sub start positions
    """
    start = 0
    while True:
        start = str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)


class Sample:
    """Class to hold data for a wit training sample.

    Attributes:
        text (str): the raw query text for the training sample
        intent (str): the user intent value for this sample
        entities (list(dict)): list of entity dictionaries containing value
            and position

    """
    def __init__(self, text, intent):
        self.text = text
        self.entities = []
        self.intent = intent

    def __repr__(self):
        return "Text: {}\nEntities: {}".format(self.text, self.entities)

    def populate_entities(self, entity_map):
        """Method to parse entities from a sample's text """
        # add secondary entities
        for word in self.text.split():
            for entity in entity_map:
                if entity in word:
                    added_str_length = 0
                    occurances = list(find_all(self.text, entity))
                    all_values = entity_map[entity]['values'].keys()
                    chosen_values = random.sample(all_values, len(occurances))
                    # for each occurance, grab a random value to put in sample
                    for i in range(len(occurances)):
                        expressions = entity_map[entity]['values'][chosen_values[i]]
                        expression = random.choice(expressions)
                        # update string
                        self.text = self.text.replace(entity, expression, 1)
                        # track resulting changes to str length
                        start = occurances[i] + added_str_length
                        added_str_length += len(expression) - len(entity)
                        # add to sample entities
                        self.entities.append({
                            "entity": entity_map[entity]['entity_type'],
                            "start": start,
                            "end": start + len(expression),
                            "value": expression
                        })
