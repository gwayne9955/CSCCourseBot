#! /usr/bin/env python

"""CSC466 Project 3 Bot"""

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
import json
import requests
import uuid
# from storage.DBProxy import DBProxy
# from intent_handling.intenthandler import IntentHandler
from spell_checker import spell_check

class TestBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        self.do_command(e, e.arguments[0])

    def on_pubmsg(self, c, e):
        a = e.arguments[0].split(":", 1)
        if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(self.connection.get_nickname()):
            self.do_command(e, a[1].strip())
        return

    def on_dccmsg(self, c, e):
        # non-chat DCC messages are raw bytes; decode as text
        text = e.arguments[0].decode('utf-8')
        c.privmsg("You said: " + text)

    def on_dccchat(self, c, e):
        if len(e.arguments) != 2:
            return
        args = e.arguments[1].split()
        if len(args) == 4:
            try:
                address = ip_numstr_to_quad(args[2])
                port = int(args[3])
            except ValueError:
                return
            self.dcc_connect(address, port)

    def do_command(self, e, cmd):
        nick = e.source.nick
        c = self.connection

        if cmd == "disconnect":
            self.disconnect()
        elif cmd == "die":
            self.die()
        elif cmd == "stats":
            for chname, chobj in self.channels.items():
                c.notice(nick, "--- Channel statistics ---")
                c.notice(nick, "Channel: " + chname)
                users = sorted(chobj.users())
                c.notice(nick, "Users: " + ", ".join(users))
                opers = sorted(chobj.opers())
                c.notice(nick, "Opers: " + ", ".join(opers))
                voiced = sorted(chobj.voiced())
                c.notice(nick, "Voiced: " + ", ".join(voiced))
        elif cmd == "dcc":
            dcc = self.dcc_listen()
            c.ctcp("DCC", nick, "CHAT chat %s %d" % (
                ip_quad_to_numstr(dcc.localaddress),
                dcc.localport))
        elif cmd == "hello": #Foaad: change this
            c.privmsg(self.channel, "greetings traveler")
        elif cmd == "about": #Foaad: add your name
            c.privmsg(self.channel, "I was made by Dr. Foaad Khosmood for the CPE 466 class in Spring 2016. I was further modified by Brett Nelson")
        elif cmd == "usage":
            #Foaad: change this
            c.privmsg(self.channel, "Hi there! Ask me information about CSC courses :(")
        else:
            with open("dialogflow.json", 'r') as j:
                api = json.load(j)

            url = (api["url"])
            id = uuid.uuid1()

            print("Hello! And welcome to the CSC Course Chatbot!")
            query = input("What question can I answer for ya?:\n")
            # run speck check over query
            query = spell_check(query)
            c.privmsg(self.channel, query)



            # db = DBProxy('credentials.txt')
            # handler = IntentHandler(db)
            # while (query.lower() != 'quit'):
            #
            #     # The http request
            #     body = {
            #         "lang": api["lang"],
            #         "query": query,
            #         "sessionId": str(id),
            #         "timezone": api["timezone"]
            #     }
            #     version = {"v": api['version']}
            #     headers = {
            #         'Authorization': "Bearer {0}".format(api["clientId"]),
            #         'Content-Type': "application/json"
            #     }
            #     response = requests.request("POST",
            #                                 url,
            #                                 data=json.dumps(body),
            #                                 headers=headers,
            #                                 params=version)
            #     if response.status_code == 200:
            #         # a valid response
            #         responseJson = json.loads(response.text)
            #
            #         # these are to be passed for further computation in the database
            #         intent = responseJson['result']['metadata']['intentName']  # a string
            #         parameters = responseJson['result']['parameters']  # a dict
            #         response = handler.handle(intent, parameters)
            #
            #         print("\nResulting intent: {0}".format(intent))
            #         print("Resulting parameters: {0}\n".format(parameters))
            #         print("Response: {}".format(response))
            #     else:
            #         print("{0} error getting response from DialogFlow\n\tReason: {1}".format(response.status_code, response.reason))


def main():
    import sys
    if len(sys.argv) != 4:
        print("Usage: testbot <server[:port]> <channel> <nickname>")
        sys.exit(1)

    s = sys.argv[1].split(":", 1)
    server = s[0]
    if len(s) == 2:
        try:
            port = int(s[1])
        except ValueError:
            print("Error: Erroneous port.")
            sys.exit(1)
    else:
        port = 6667
    channel = sys.argv[2]
    nickname = sys.argv[3]

    bot = TestBot(channel, nickname, server, port)
    bot.start()

if __name__ == "__main__":
    main()
