from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from requests.exceptions import ConnectionError
from wtforms import StringField, IntegerField, DecimalField, SelectField
from wtforms.validators import DataRequired

import urllib.request
import json


class ClientDataForm(FlaskForm):
    state = StringField('State', validators=[DataRequired()])
    acc_length = IntegerField('Account length', validators=[DataRequired()])
    area_code = IntegerField('Area code', validators=[DataRequired()])
    int_plan = SelectField('International plan', choices=[('No', 'No'), ('Yes', 'Yes')], validate_choice=True)
    voice_mail_plan = SelectField('Voice mail plan', choices=[('No', 'No'), ('Yes', 'Yes')], validate_choice=True)
    v_messages = IntegerField('Number vmail messages', validators=[DataRequired()])

    t_d_minutes = DecimalField('Total day minutes', validators=[DataRequired()])
    t_d_calls = IntegerField('Total day calls', validators=[DataRequired()])
    t_d_charge = DecimalField('Total day charge', validators=[DataRequired()])

    t_e_minutes = DecimalField('Total eve minutes', validators=[DataRequired()])
    t_e_calls = IntegerField('Total eve calls', validators=[DataRequired()])
    t_e_charge = DecimalField('Total eve charge', validators=[DataRequired()])

    t_n_minutes = DecimalField('Total night minutes', validators=[DataRequired()])
    t_n_calls = IntegerField('Total night calls', validators=[DataRequired()])
    t_n_charge = DecimalField('Total night charge', validators=[DataRequired()])

    t_i_minutes = DecimalField('Total intl minutes', validators=[DataRequired()])
    t_i_calls = IntegerField('Total intl calls', validators=[DataRequired()])
    t_i_charge = DecimalField('Total intl charge', validators=[DataRequired()])

    cs_calls = IntegerField('Customer service calls', validators=[DataRequired()])


app = Flask(__name__)
app.config.update(
    CSRF_ENABLED=True,
    SECRET_KEY='you-will-never-guess',
)


def get_prediction(state, acc_length, area_code, int_plan, voice_mail_plan, v_messages, t_d_minutes, t_d_calls,
                   t_d_charge,
                   t_e_minutes, t_e_calls, t_e_charge, t_n_minutes, t_n_calls, t_n_charge, t_i_minutes, t_i_calls,
                   t_i_charge, cs_calls):
    body = {'state': state, 'account_length': acc_length, 'area_code': area_code, 'international_plan': int_plan,
            'voice_mail_plan': voice_mail_plan, 'number_vmail_messages': v_messages, 'total_day_minutes': t_d_minutes,
            'total_day_calls': t_d_calls, 'total_day_charge': t_d_charge, 'total_eve_minutes': t_e_minutes,
            'total_eve_calls': t_e_calls, 'total_eve_charge': t_e_charge, 'total_night_minutes': t_n_minutes,
            'total_night_calls': t_n_calls, 'total_night_charge': t_n_charge, 'total_intl_minutes': t_i_minutes,
            'total_intl_calls': t_i_calls, 'total_intl_charge': t_i_charge, 'customer_service_calls': cs_calls}

    myurl = "http://0.0.0.0:8180/predict"
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')  # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    # print (jsondataasbytes)
    response = urllib.request.urlopen(req, jsondataasbytes)
    return json.loads(response.read())['predictions']


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/predicted/<response>')
def predicted(response):
    response = json.loads(response)
    print(response)
    return render_template('predicted.html', response=response)


@app.route('/predict_form', methods=['GET', 'POST'])
def predict_form():
    form = ClientDataForm()
    data = dict()
    if request.method == 'POST':
        data['state'] = request.form.get('state')
        data['account_length'] = request.form.get('acc_length')
        data['area_code'] = request.form.get('area_code')
        data['international_plan'] = request.form.get('int_plan')
        data['voice_mail_plan'] = request.form.get('voice_mail_plan')
        data['number_vmail_messages'] = request.form.get('v_messages')
        data['total_day_minutes'] = request.form.get('t_d_minutes')
        data['total_day_calls'] = request.form.get('t_d_calls')
        data['total_day_charge'] = request.form.get('t_d_charge')
        data['total_eve_minutes'] = request.form.get('t_e_minutes')
        data['total_eve_calls'] = request.form.get('t_e_calls')
        data['total_eve_charge'] = request.form.get('t_e_charge')
        data['total_night_minutes'] = request.form.get('t_n_minutes')
        data['total_night_calls'] = request.form.get('t_n_calls')
        data['total_night_charge'] = request.form.get('t_n_charge')
        data['total_intl_minutes'] = request.form.get('t_i_minutes')
        data['total_intl_calls'] = request.form.get('t_i_calls')
        data['total_intl_charge'] = request.form.get('t_i_charge')
        data['customer_service_calls'] = request.form.get('cs_calls')

        try:
            response = str(
                get_prediction(data['state'], data['account_length'], data['area_code'], data['international_plan'],
                               data['voice_mail_plan'], data['number_vmail_messages'],
                               data['total_day_minutes'], data['total_day_calls'], data['total_day_charge'],
                               data['total_eve_minutes'], data['total_eve_calls'], data['total_eve_charge'],
                               data['total_night_minutes'], data['total_night_calls'],
                               data['total_night_charge'], data['total_intl_minutes'],
                               data['total_intl_calls'], data['total_intl_charge'],
                               data['customer_service_calls']))
            print(response)
        except ConnectionError:
            response = json.dumps({"error": "ConnectionError"})
        return redirect(url_for('predicted', response=response))
    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8181, debug=True)
