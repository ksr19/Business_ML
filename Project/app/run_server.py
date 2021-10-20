# USAGE
# Start the server:
# 	python run_front_server.py
# Submit a request via Python:
#	python simple_request.py

# import the necessary packages
import dill
import pandas as pd
import numpy as np
import os
import flask
import logging
from logging.handlers import RotatingFileHandler
from time import strftime

dill._dill._reverse_typemap['ClassType'] = type

# initialize our Flask application and the model
app = flask.Flask(__name__)
# app.debug = True
model = None

handler = RotatingFileHandler(filename='app.log', maxBytes=1000000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def load_model(model_path):
    # load the pre-trained model
    global model
    # with open(model_path, 'rb', encoding='utf-8') as f:
    #     model = dill.load(f)
    with open(model_path, 'rb') as f:
        model = dill.load(f)
    print(model)


modelpath = "/app/app/models/gb_model.dill"
load_model(modelpath)


@app.route("/", methods=["GET"])
def general():
    return """Welcome to custom transaction prediction page. Please use 'http://<address>/predict' to POST"""


@app.route("/predict", methods=["POST"])
def predict():
    # initialize the data dictionary that will be returned from the
    # view

    data = {"success": False}
    values = {}
    dt = strftime("[%Y-%b-%d %H:%M:%S]")
    # # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":

        fields = ['State', 'Account length', 'Area code', 'International plan',
                  'Voice mail plan', 'Number vmail messages', 'Total day minutes',
                  'Total day calls', 'Total day charge', 'Total eve minutes',
                  'Total eve calls', 'Total eve charge', 'Total night minutes',
                  'Total night calls', 'Total night charge', 'Total intl minutes',
                  'Total intl calls', 'Total intl charge', 'Customer service calls']
        for field in fields:
            values[field] = ""

        request_json = flask.request.get_json()
        if request_json["state"]:
            values['State'] = request_json['state']

        if request_json["account_length"]:
            values['Account length'] = float(request_json['account_length'])

        if request_json["area_code"]:
            values['Area code'] = int(request_json['area_code'])

        if request_json["international_plan"]:
            values['International plan'] = request_json['international_plan']

        if request_json["voice_mail_plan"]:
            values['Voice mail plan'] = request_json['voice_mail_plan']

        if request_json["number_vmail_messages"]:
            values['Number vmail messages'] = float(request_json['number_vmail_messages'])

        if request_json["total_day_minutes"]:
            values['Total day minutes'] = float(request_json['total_day_minutes'])

        if request_json["total_day_calls"]:
            values['Total day calls'] = float(request_json['total_day_calls'])

        if request_json["total_day_charge"]:
            values['Total day charge'] = float(request_json['total_day_charge'])

        if request_json["total_eve_minutes"]:
            values['Total eve minutes'] = float(request_json['total_eve_minutes'])

        if request_json["total_eve_calls"]:
            values['Total eve calls'] = float(request_json['total_eve_calls'])

        if request_json["total_eve_charge"]:
            values['Total eve charge'] = float(request_json['total_eve_charge'])

        if request_json["total_night_minutes"]:
            values['Total night minutes'] = float(request_json['total_night_minutes'])

        if request_json["total_night_calls"]:
            values['Total night calls'] = float(request_json['total_night_calls'])

        if request_json["total_night_charge"]:
            values['Total night charge'] = float(request_json['total_night_charge'])

        if request_json["total_intl_minutes"]:
            values['Total intl minutes'] = float(request_json['total_intl_minutes'])

        if request_json["total_intl_calls"]:
            values['Total intl calls'] = float(request_json['total_intl_calls'])

        if request_json["total_intl_charge"]:
            values['Total intl charge'] = float(request_json['total_intl_charge'])

        if request_json["customer_service_calls"]:
            values['Customer service calls'] = float(request_json['customer_service_calls'])

        logger.info(f'{dt} Data: {values}')
        print(model)
        try:
            preds = model.predict_proba(pd.DataFrame(values, index=[0]))
        #
        except AttributeError as e:
            logger.warning(f'{dt} Exception: {str(e)}')
            data['predictions'] = str(e)
            data['success'] = False
            return flask.jsonify(data)

        data["predictions"] = np.round(preds[:, 1][0], 6) * 100
        # indicate that the request was a success
        data["success"] = True

    # return the data dictionary as a JSON response
    return flask.jsonify(data)


# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
    print(("* Loading the model and Flask starting server..."
           "please wait until server has fully started"))
    port = int(os.environ.get('PORT', 8180))
    app.run(host='0.0.0.0', debug=True, port=port)
