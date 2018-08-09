import json
import requests

def processRequest(req):
    print("Request:")
    print(json.dumps(req, indent=4))
    print(req.get("queryResult").get("intent"))
    if req.get("queryResult").get("intent") == "projects/oftheinstrument/agent/intents/4bd6e615-a3f2-43a0-aec3-486e824ef015":
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