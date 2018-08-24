import flask
import json
import requests
import time
from rover import Rover

application = flask.Flask(__name__)

rovers = {1: Rover(1)}
currentRover = 1


@application.route('/')
def getStatus():
    print("Hello? Can anyone hear me?")
    return "Hello, I am running...:"

@application.route('/control', methods=['GET'])
def controller():
    global rovers
    req = flask.request.args
    
    roverid = int(req.get("roverid"))
    if roverid not in rovers.keys():
        rovers[roverid] = Rover(roverid)

    rovers[roverid].updateData(
        req.get("left"),
        req.get("right"),
        req.get("duration")
    )

    res = "Moved!"
    return res


@application.route('/getcommands', methods=['GET'])
def returnCommand():
    global rovers

    req = flask.request.args
    print(req)

    roverid = int(req.get("roverid"))
    print(rovers[roverid].postData(reset=False))

    if roverid not in rovers.keys():
        rovers[roverid] = Rover(roverid)

    res = rovers[roverid].postData()

    if req.get("kill"):
        del rovers[roverid]
        return

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
        assignCommand(req, 255, 255)
        res = speech("Sallying forth!")

    elif action == "turn":
        direction = req["result"]["parameters"]["direction"]
        if direction == "left":
            assignCommand(req, -255, 255)
            res = speech("Turning left!")
        elif direction == "right":
            assignCommand(req, 255, -255)
            res = speech("Turning right!")

    elif action == "retreat":
        assignCommand(req, -255, -255)
        res = speech("Going back!")
    
    elif action == "halt":
        assignCommand(req, 0, 0)
        res = speech("Stopping!")
    
    elif action == "openClaw":
        assignCommand(req, claw=0)
    
    elif action == "closeClaw":
        assignCommand(req, claw=1)
    
    elif action == "numberOfRovers":
        if len(rovers) == 1:
            res = speech("There is 1 rover connected to the server.")
        else:
            res = speech("There are " + str(len(rovers)) + " connected to the server.")
    
    elif action == "activeRovers":
        activeRovers = 0
        for rover in rovers.values():
            if rover.isMoving():
                activeRovers += 1

        if activeRovers == 1:
            activeSpeech = "There is 1 rover moving at the moment."
        else:
            activeSpeech = "There are " + str(activeRovers) + " rovers moving at the moment."

        if len(rovers)-activeRovers == 1:
            stoppedSpeech = "There is 1 inactive rover."
        else:
            stoppedSpeech = "There are " + str(len(rovers)-activeRovers) + " inactive rovers."
        
        res = speech(activeSpeech + "\n" + stoppedSpeech)

    else:
        res = speech("Oops, I didn't get that...")

    return res

def assignCommand(req, left=0, right=0, claw=0):
    global rovers, currentRover
    travelTime = 5

    roverid = currentRover

    if len(req["result"]["parameters"]["duration"]) > 1:
        duration = req["result".get("parameters").get("duration")
    
        if duration["unit"] == "s":
            travelTime = duration["amount"]
        elif duration["unit"] == "min":
            travelTime = duration["amount"] * 60
    
    print(roverid, rovers.keys())
        
    if roverid in rovers.keys():
        print(roverid)
        rovers[roverid].updateData(left, right, travelTime, claw)

def speech(speech):
    return {
        "speech": speech,
        "displayText": speech,
        "source": "webhookdata"
    }

        

if __name__ == '__main__':
    application.run()