import json
import requests

api_key = "aa7ba7c6056c4861b9d004841e7a4d50"
endpoint = "https://api.cognitive.microsoft.com/bing/v7.0/spellcheck"

params = {
    'mkt':'en-us',
    'mode':'proof'
}

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Ocp-Apim-Subscription-Key': api_key,
}

CORRECTION_THRESHOLD = 0.85

def correct_text(text, json_response):
    string_len_change = 0
    for flagged in json_response['flaggedTokens']:
        pos = int(flagged['offset']) + string_len_change
        token_len = len(flagged['token'])
        suggestions = flagged['suggestions']
        if len(suggestions) > 0:
            suggest = suggestions[0]
            substitute = str(suggest['suggestion'])
            if float(suggest['score']) > CORRECTION_THRESHOLD:
                text = text[:pos] + substitute + text[pos + token_len:]
                string_len_change += len(substitute) - token_len
    return text

def spell_check(text):
    data = {'text': text}
    response = requests.post(endpoint, headers=headers, params=params, data=data)
    json_response = response.json()
    return correct_text(text, json_response)
