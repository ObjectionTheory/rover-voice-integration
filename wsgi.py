import flask
import json
import requests
import time
from rover import Rover

application = flask.Flask(__name__)

rovers = {1: Rover(1)}


@application.route('/')
def get_status():
    print("Hello? Can anyone hear me?")
    return "Hello, I am running..." + time.time()



'''
@application.route('/commands')
def display_commands():
    commands = "\n".join([rover.postData for rover in rovers])
    return commands
'''
@application.route('/webhooks', methods=['POST'])
def webhook():
    
    req = flask.request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))
    
    print("Break1")
    res = webhooks.processRequest(req)
    print("Break3")
    print(flask.jsonify(res))
    return flask.jsonify(res)

def processRequest(req):
    print("Request:")
    print(json.dumps(req, indent=4))

    roverid = req.get("result").get("parameters").get("roverid")

    if req.get("result").get("metadata").get("intentName") == "Sally Forth!":
        travelTime = 5
        if len(req.get("result").get("parameters").get("duration")) > 1:
            duration = req.get("result").get("parameters").get("duration")
       
            if duration.get("unit") == "s":
                travelTime = duration.get("amount")
            elif duration.get("unit") == "min":
                travelTime = duration.get("amount") * 60
        
        rovers[roverid].updateData("{}:{}".format((255,255), travelTime))

        text = "Sallying forth!"
        
        print("Yeet")
        res = speech(text)
    else:
        res = speech("Oops, I didn't get that...")

    print(res)
    return res

def speech(speech):
    return {
        "speech": speech,
        "displayText": speech,
        "source": "webhookdata"
    }

        

if __name__ == '__main__':
    application.run()