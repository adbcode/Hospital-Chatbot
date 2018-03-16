from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import apiai
import json
import os
import sys

from flask import Flask
from flask import request
from flask import make_response

import sqlite3

# Flask app should start in global layout
app = Flask(__name__)

CLIENT_ACCESS_TOKEN = 'c0dce7652e6b4a16b3e818ff84b78373'
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

conn = sqlite3.connect('hospital.db')

@app.route('/')
def Main():
    return render_template("homepage.html")

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "yahooWeatherForecast":
        return {}
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = makeYqlQuery(req)
    if yql_query is None:
        return {}
    yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    result = urlopen(yql_url).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res


def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def makeWebhookResult(data):
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}

    condition = item.get('condition')
    if condition is None:
        return {}

    # print(json.dumps(item, indent=4))

    speech = "Today the weather in " + location.get('city') + ": " + condition.get('text') + \
             ", And the temperature is " + condition.get('temp') + " " + units.get('temperature')

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }

# list of functions to be implemented
# - booking appointments
# - query doctors - their schedules, etc.
# - query meds - info, availability, etc.
# - basic medical help
# - query hospital location, contact details, etc.

# Booking appointments
def book(data):
	# Assuming data contains 
	# PID, DID, HID, PURPOSE, ADATETIME, AFEE
	# in that order
	return "INSERT INTO APPOINTMENT(PID, DID, HID, PURPOSE, ADATETIME, AFEE) \
		VALUES (%s, %s, %s, %s, %s, %s)", (data[0], data[1], data[2], data[3], data[4], data[5]))

# Getting list of doctors of given specialty in a certain hospita
def doctor_list(data):
	# Assuming data contains
	# HID, DSPECIAL
	return "SELECT DNAME, DFEE FROM DOCTOR WHERE HID = %s AND DSPECIAL = %s", (data[0], data[1])

# Get a doctor's schedule
def doctor_schedule(data):
	# Assuming data contains
	# DID
	return "SELECT WEEKDAY, TIME FROM DOCTOR WHERE DID = %s", (data[0])
	
# Query a medicine
def medicine(data):
	# Assuming data contains
	# MID
	return "SELECT MNAME, MDOSAGE, MPRICE FROM MEDICINE WHERE MID = %s", (data[0])

# Query basic medical help
def medihelp(data):
	# Assuming data contains
	# SID
	return "SELECT MNAME, MDOSAGE, MPRICE FROM MEDICINE WHERE MID = SELECT SMED \
		FROM SYMPTOMS WHERE SID = %s", (data[0])

# Query hospital location, contact details
def hospital(data):
	# Assuming data contains
	# HID
	return "SELECT HLOCATION, HPHONE FROM HOSPITAL WHERE HID = %s", (data[0])

#if __name__ == '__main__':
#    port = int(os.getenv('PORT', 5000))
#
#   print("Starting app on port %d" % port)
#
#   app.run(debug=False, port=port, host='0.0.0.0')

	
if __name__ == '__main__':
    app.run(debug=True,ssl_context='adhoc')