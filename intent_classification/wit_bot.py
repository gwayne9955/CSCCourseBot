import json
import sample
import wit_wrapper

entity_map = json.load(open('entity_map.json', 'r'))
sample_map = json.load(open('sample_map.json', 'r'))


def message_bot(message):
    """Send message to wit bot and parse response
    Args:
        message (str): a query for wit bot to handle

    Returns:
        dict with parsed response data
    """
    message_data = {}
    r = wit_wrapper.message(message)
    if r.status_code != 200:
        print("Error {} from wit".format(r.status_code))
        print(r.content)
    return json.loads(r.content.decode('UTF-8'))


def create_entities():
    """Create wit bot entities"""
    for entity in entity_map:
        r = wit_wrapper.create_entity(entity_map[entity]['wit_entity'],
                                  entity_map[entity]['description'])
        if r.status_code != 200:
            print("Error {} from wit".format(r.status_code))
            print(r.content)


def update_entity_values():
    """Update wit bot's entities"""
    for entity in entity_map:
        values = entity_map[entity]['values']
        for value in values:
            # update wit bot entity
            r = wit_wrapper.add_entity_values(entity_map[entity]['wit_entity'],
                                              (value, values[value]))
            if r.status_code != 200:
                print("Error {} from wit".format(r.status_code))
                print(r.content)


def update_samples():
    """Update wit bot's samples"""
    samples = []
    # loop through sample keys
    for sample_key in sample_map:
        intent = sample_map[sample_key]['intent']
        rephrases = sample_map[sample_key]['rephrases']
        # create a sample for each phrase
        for phrase in rephrases:
            s = sample.Sample(phrase, intent)
            s.populate_entities(entity_map)
            samples.append(s)

    batch_size = 5
    num_batches = len(samples) // batch_size + 1
    for i in range(num_batches):
        if i == num_batches - 1:
            batch = samples[i*batch_size:]
        else:
            batch = samples[i*batch_size:(i+1)*batch_size]
        r = wit_wrapper.train(batch)
        if r.status_code != 200:
            print("Error {} from wit:".format(r.status_code))
            print(r.content)


def update_bot():
    """Update wit bot data"""
    update_entity_values()
    update_samples()


# create_entities()
# update_bot()
message_bot("Is CSC 357 available in winter quarter?")
