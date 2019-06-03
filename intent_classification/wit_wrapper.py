import requests

wit_access_token = 'KVKU7OBSJ76ACQJ22KXAH5VZO4ZREG4F'
authorization = 'Bearer {}'.format(wit_access_token)


def message(message):
    """Query qit bot for meaning of a sentence
    Args:
        text (str): the text to query

    Returns:
        response from wit
    """
    q = message.replace(' ', '%20')
    url = "https://api.wit.ai/message?v=20170307&q={}".format(q)
    return requests.get(url=url, headers={'Authorization': authorization})


def train(samples):
    """Method that trains wit bot on given samples.

    Args:
        samples (list(Sample)): list of samples to train on
    """
    url = 'https://api.wit.ai/samples?v=20170307'
    headers = {
        'Authorization': authorization,
        'Content-Type': 'application/json'
    }
    data = []
    for sample in samples:
        data.append({
            "text": sample.text,
            "entities": sample.entities
        })
    return requests.post(url=url, json=data, headers=headers)


def create_entity(name, doc):
    """Create new entity"""
    url = 'https://api.wit.ai/entities?v=20170307'
    headers = {
        'Authorization': authorization,
        'Content-Type': 'application/json'
    }
    data = {'id': name, 'doc': doc}
    r = requests.post(url=url, json=data, headers=headers)


def add_entity_values(entity, val):
    """Add values to a wit bot entity

    Args:
        entity (str): entity value to update
        val ((str, [list(str)])): list of tuples, with
            str being a value name and list(str) being
            a list of possible ways to express that value

    Example:
        add_entity_values("course", ("CSC_357", ["CSC 357", "CPE 357",
            "Systems Programming"]))
    """
    url = 'https://api.wit.ai/entities/{}/values?v=20170307'.format(entity)
    headers = {
        'Authorization': authorization,
        'Content-Type': 'application/json'
    }
    if len(val[1]) > 0:
        data = {
            "value": val[0],
            "expressions": val[1]
        }
    else:
        data = {"value": val[0]}
    return requests.post(url=url, json=data, headers=headers)
