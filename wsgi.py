import flask
import json
import webhooks

application = flask.Flask(__name__)


@application.route('/')
def get_status():
    print("Hello? Can anyone hear me?")
    return "Hello, I am running..."

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
    

if __name__ == '__main__':
    application.run()