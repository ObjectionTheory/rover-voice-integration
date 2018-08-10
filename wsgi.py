import flask
import json
import requests
import time
from rover import Rover

application = flask.Flask(__name__)

rovers = {1: Rover(1),
        2: Rover(2)}


@application.route('/')
def getStatus():
    print("Hello? Can anyone hear me?")
    return "Hello, I am running...:{}".format(time.time())


@application.route('/commands', methods=['POST'])
def returnCommand():
    global rovers
    req = flask.request.get_json(silent=True, force=True)

    roverid = req["roverid"]

    res = rovers[roverid].postData()

    return flask.jsonify(res)
    

@application.route('/webhooks', methods=['GET'])
def webhook():
    
    req = flask.request.args
    if req["roverid"]:    
        res = webhooks.processRequest(req)

        return flask.jsonify(res)
    else:
        return

def processRequest(req):
    print("Request:")
    print(json.dumps(req, indent=4))

    intent = ["result"]["metadata"]["intentName"]

    if intent == "Sally Forth!":
        move(255, 255, req)
        res = speech("Sallying forth!")

    elif intent == "Turn!":
        direction = req["result"]["parameters"]["direction"]
        if direction == "left":
            move(-255, 255, req)
            res = speech("Turning left!")
        elif direction == "right":
            move(255, -255, req)
            res = speech("Turning right!")

    elif intent == "Retreat!":
        move(-255, -255, req)
        res = speech("Going back!")

    else:
        res = speech("Oops, I didn't get that...")

    return res

def move(left, right, req):
    global rovers
    travelTime = 5

    if len(req["result"]["parameters"]["duration"]) > 1:
        duration = req["result"]["parameters"]["duration"]
    
        if duration["unit"] == "s":
            travelTime = duration["amount"]
        elif duration["unit"] == "min":
            travelTime = duration["amount"] * 60
    
    roverid = req["result"]["parameters"]["roverid"]
    if roverid in rovers.keys():
        rovers[roverid].updateData(left, right, duration)

def speech(speech):
    return {
        "speech": speech,
        "displayText": speech,
        "source": "webhookdata"
    }

        

if __name__ == '__main__':
    application.run()