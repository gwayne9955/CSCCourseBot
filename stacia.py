# The command line interface for Project 3

import json
import requests
import uuid
from storage.DBProxy import DBProxy
from intent_handling.intenthandler import IntentHandler
from intent_handling.teamdelegation import best_team_estimate

def main():
    with open("dialogflow.json", 'r') as j:
        api = json.load(j)

    url = (api["url"])
    id = uuid.uuid1()

    print("Hello! And welcome to the CSC Course Chatbot!")
    query = input("What question can I answer for ya?:\n")
    db = DBProxy('credentials.txt')
    handler = IntentHandler(db)
    while (query.lower() != 'quit'):

        # The http request
        body = {
            "lang": api["lang"],
            "query": query,
            "sessionId": str(id),
            "timezone": api["timezone"]
        }
        version = {"v": api['version']}
        headers = {
            'Authorization': "Bearer {0}".format(api["clientId"]),
            'Content-Type': "application/json"
        }
        response = requests.request("POST",
                                    url,
                                    data=json.dumps(body),
                                    headers=headers,
                                    params=version)
        if response.status_code == 200:
            # a valid response
            responseJson = json.loads(response.text)

            # these are to be passed for further computation in the database
            intent = responseJson['result']['metadata']['intentName']  # a string
            parameters = responseJson['result']['parameters']  # a dict
            response = handler.handle(intent, parameters)

            if response is None:
                team = best_team_estimate(query)
                if team is None:
                    response = "Sorry, I'm not sure how to answer that."
                else:
                    response = 'The {} bot might be able to answer that question for you.'.format(team)

            print("\nResulting intent: {0}".format(intent))
            print("Resulting parameters: {0}\n".format(parameters))
            print("Response: {}".format(response))
        else:
            print("{0} error getting response from DialogFlow\n\tReason: {1}".format(response.status_code, response.reason))

        query = input("What question can I answer for ya?:\n")

    print("Goodbye and thank you for using our CSC Course Chatbot")

if __name__ == '__main__':
    main()
