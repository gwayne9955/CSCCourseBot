# The command line interface for Project 3

import json
import requests
import uuid
from storage.DBProxy import DBProxy
from intent_handling.intenthandler import IntentHandler
from spell_checker import spell_check
from intent_handling.teamdelegation import best_team_estimate
from intent_handling.signal import Signal


class Stacia:
    def __init__(self):
        with open("dialogflow.json", 'r') as j:
            self.api = json.load(j)

        self.url = (self.api["url"])
        self.id = uuid.uuid1()

        db = DBProxy('credentials.txt')
        self.handler = handler = IntentHandler(db)

    def respond(self, query) -> str:
        query = spell_check(query)

        # The http request
        body = {
            "lang": self.api["lang"],
            "query": query,
            "sessionId": str(id),
            "timezone": self.api["timezone"]
        }
        version = {"v": self.api['version']}
        headers = {
            'Authorization': "Bearer {0}".format(self.api["clientId"]),
            'Content-Type': "application/json"
        }
        httpResponse = requests.request("POST",
                                    self.url,
                                    data=json.dumps(body),
                                    headers=headers,
                                    params=version)
        if httpResponse.status_code == 200:
            # a valid response
            responseJson = json.loads(httpResponse.text)

            # these are to be passed for further computation in the database
            intent = responseJson['result']['metadata']['intentName']  # a string
            parameters = responseJson['result']['parameters']  # a dict
            response = self.handler.handle(intent, parameters)

            if response is None:
                team = best_team_estimate(query)
                if team is None:
                    response = Signal.ERROR, "Sorry, I'm not sure how to answer that."
                else:
                    response = Signal.NORMAL, 'The {} bot might be able to answer that question for you.'.format(team)

            #print("\nResulting intent: {0}".format(intent))
            #print("Resulting parameters: {0}\n".format(parameters))

            return response
        else:
            return Signal.ERROR, "{0} error getting response from DialogFlow\n\tReason: {1}".format(
                response.status_code, response.reason)


def main():
    print("Hello! And welcome to the CSC Course Chatbot!")
    stacia = Stacia()
    query = input("What question can I help answer for you?:\n")
    while (query.lower() != 'quit'):
        if query == 'help':
            helpStr = """Example questions about the Cal Poly CSC Course System you can ask me:\n
                \t• \'Does CSC 349 satisfy GE Area a2?\'
                \t• \'What class title is given to CSC 466?\'
                \t• \'When is CSC 453 typically offered?\'
                \t• \'Which courses require junior standing?\'
                \t• \'What code does computer graphics have?\'"""
            print(helpStr)
        else:
            response = stacia.respond(query)
            print("{}".format(response[1]))
            query = input("What question can I help answer for you?:\n")

    print("Goodbye and thank you for using our CSC Course Chatbot")


if __name__ == '__main__':
    main()
