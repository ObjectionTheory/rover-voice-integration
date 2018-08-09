import json
import requests

def processRequest(req):
    print("Request:")
    print(json.dumps(req, indent=4))

    
    if req.get("result").get("metadata").get("intentName") == "Sally Forth!":
        print("Yeet")
        res = speech("Sallying forth!")
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