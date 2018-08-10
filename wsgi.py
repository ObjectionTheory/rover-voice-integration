import flask
import json
import requests
import time
from rover import Rover

application = flask.Flask(__name__)

rovers = {1: Rover(1)}


@application.route('/')
def getStatus():
    print("Hello? Can anyone hear me?")
    return "Hello, I am running...:"


@application.route('/commands', methods=['GET'])
def returnCommand():
    global rovers

    req = flask.request.args
    print(req)

    roverid = int(req.get("roverid"))

    if roverid not in rovers.keys():
        rovers[roverid] = Rover(roverid)

    res = rovers[roverid].postData()

    return flask.jsonify(res)
    

@application.route('/webhooks', methods=['POST'])
def webhook():
    
    req = flask.request.get_json(silent=True, force=True)
    
    res = processRequest(req)

    return flask.jsonify(res)

def processRequest(req):
    print("Request:")
    print(json.dumps(req, indent=4))

    action = req["result"]["action"]

    if action == "sallyForth":
        move(255, 255, req)
        res = speech("Sallying forth!")

    elif action == "turn":
        direction = req["result"]["parameters"]["direction"]
        if direction == "left":
            move(-255, 255, req)
            res = speech("Turning left!")
        elif direction == "right":
            move(255, -255, req)
            res = speech("Turning right!")

    elif action == "retreat":
        move(-255, -255, req)
        res = speech("Going back!")
    
    elif action == "halt":
        move(0, 0, req)
        res = speech("Stopping!")
    
    elif action == "numberOfRovers":
        res = speech("There are " + str(len(rovers)) + " active.")
        

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