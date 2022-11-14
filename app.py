import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from urllib.request import urlopen
import http.client
import base64
import time
import ast
import json

conn = http.client.HTTPSConnection("misguided.enterprises")
payload = ''
headers = {}

slackMap = {'e-lee-za': 'UTZBECLA2',
            'silversaw': 'U0176N7HS1F'
            }

cursor = int(time.time())

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


def gib_lookout():
    global cursor;
    conn.request("GET", "/hkgi/activity", payload, headers)
    res = conn.getresponse()
    data = res.read()

    activity = json.loads(data.decode("utf-8"))
    for event in activity:
        if event["kind"] == "gib":
            if event["ts"] <= cursor:
                pass
            else:
                print(event["from"], "sent", event["to"], event["amount"], event["item"])

                conn.request("GET", "/hksl/user?username={}".format(event["to"], payload, headers))
                res = conn.getresponse()
                data = res.read()
                userinfo = json.loads(data.decode("utf-8"))
                slackID = userinfo["user"]["slackId"]

                app.client.chat_postMessage(channel=slackID,
                                   text="{0} sent you {1} {2}!".format(event["from"], event["amount"], event["item"]))
                
                cursor = event["ts"]+1

#app.client.chat_postMessage(channel="UTZBECLA2", text="hello world!")

running = True
while running:
    gib_lookout()


# Start your app
# if __name__ == "__main__":
#    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
