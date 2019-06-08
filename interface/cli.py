# The command line interface for Project 3

import json
import requests
import uuid

def main():
    with open("dialogflow.json", 'r') as j:
        api = json.load(j)

    url = (api["url"])
    id = uuid.uuid1()

    print("Hello! And welcome to the CSC Course Chatbot!")
    query = input("What question can I answer for ya?:\n")
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
            'Authorization': "Bearer 461c339b64ce4f96bf44502fbb9b0a23",
            'Content-Type': "application/json"
        }
        response = requests.request("POST",
                                    url,
                                    data=json.dumps(body),
                                    headers=headers,
                                    params=version)
        responseJson = json.loads(response.text)

        # these are to be passed for further computation in the database
        intent = responseJson['result']['metadata']['intentName']  # a string
        parameters = responseJson['result']['parameters']  # a dict

        print("\nResulting intent: {0}".format(intent))
        print("Resulting parameters: {0}\n".format(parameters))

        query = input("What question can I answer for ya?:\n")

    print("Goodbye and thank you for using our CSC Course Chatbot")


if __name__ == '__main__':
    main()