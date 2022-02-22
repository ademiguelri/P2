from unittest import result
from flask import Flask, request, abort, jsonify, make_response
from flask_cors import CORS
import queue
from config import get_config
import os
from opcua import Client
from opcua import ua

app = Flask(__name__)
CORS(app)
results = dict()
lines = dict()

@app.route('/variable', methods=['POST'])
def post_variable( ):
    global config
    client = Client(config.opcua_host)
    client.connect()
    in_data = request.get_json()
    var = client.get_node(in_data["nodeId"])
    if in_data["operation"] == "SET":
        var.set_value(in_data["value"])
    elif in_data["operation"] == "INC":
        current_value = var.get_value()
        if "value" in in_data:
            var.set_value(current_value+in_data["value"])
        else:
            var.set_value(current_value+1)
    elif in_data["operation"] == "DEC":
        current_value = var.get_value()
        if "value" in in_data:
            var.set_value(current_value-in_data["value"])
        else:
            var.set_value(current_value-1)
    client.disconnect()
    return "{}"

if __name__ == '__main__':
    env = os.environ.get("ENV", "DEVELOPMENT")
    config = get_config(env)
    lines = dict()
    results = dict()
    app.config.from_object(config)
    app.run("0.0.0.0", port=5000, threaded=True, debug=True)
