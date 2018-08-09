def processRequest(req):
    print('BeforeAuth')
    auth = utils.perform_basic_auth()
    print("AfterAuth")
    print("Request:")
    print(json.dumps(req, indent=4))
    
    if req.get("result").get("action") == "task_number":
        res = taskNumber(req, auth)
    else:
        speech = "Oops. Something wrong happened..."
        return {
            "speech": speech,
            "displayText": speech,
            "source": "webhookdata"
        }

    return res