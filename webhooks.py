import json
import requests

def processRequest(req):
    print("Request:")
    print(json.dumps(req, indent=4))
    
    if req.get("result").get("action") == "SallyForth":
        print("Yeet")
        res = speech("Sallying forth!")
    else:
        return speech("Oops, I didn't get that...")

    return res

def speech(speech):
    return {
        "speech": speech,
        "displayText": speech,
        "source": "webhookdata"
    }