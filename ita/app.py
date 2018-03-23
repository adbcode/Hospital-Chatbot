#!/usr/bin/env python
# coding:utf-8

import urllib
import json
from flask import *
import json,requests,sys
import apiai
import sqlite3

app = Flask(__name__)

CLIENT_ACCESS_TOKEN = 'c0dce7652e6b4a16b3e818ff84b78373'

ai= apiai.ApiAI(CLIENT_ACCESS_TOKEN)
conn = sqlite3.connect('hospital.db')

@app.route('/')
def main():
	return render_template('homepage.html')

@app.route('/webhook',methods=["POST"])
def webhook():
	req = request.get_json(silent=True, force=True)
	#print "Request:"
	#print json.dumps(req, indent=4)
	res = makeWebhookResult(req)
	res = json.dumps(res, indent=4)
	#print res
	r = make_response(res)
	r.headers['Content-Type'] = 'application/json'
	return r


def makeWebhookResult(req):
	#if req.get("result").get("action")!="interest":
	#	return {}
	stri = req.get("result").get("action")
	if stri=="interest":
		result = req.get("result")
		parameters = result.get("parameters")
		zone = parameters.get("bank-name")
		bank = {'Federal bank': '6.4%', 'Andhra bank': '10.56'}
		speech = "the intrest rate of " + zone + " " +str(bank[zone])
		print("Response:")
		print(speech)
		return {
			"speech" : speech,
			"displayText": speech,
			"source": "Healthmaster"
		}
	if stri=="places":
		result = req.get("result")
		parameters = result.get("parameters")
		location = str(parameters.get("locations"))
		dictionary = {"mangalore" : 1, "panaji" : 2, "jaipur" : 3, "salem" : 4, "vijayawada" : 5}
		if location in dictionary.keys():
			hid = dictionary[location.lower()]
			conn = sqlite3.connect('hospital.db')
			cursor = conn.execute("SELECT HLOCATION, HPHONE FROM HOSPITAL WHERE HID = " + str(hid))
			data = cursor.fetchone()
			speech = "Hospital is located at: " + data[0] + "\nContact Details: " + str(data[1])
		else:
			speech = "There is no hospital in the given location."
		print("Response:")
		print(speech)
		return {
			"speech" : speech,
			"displayText": speech,
			"source": "Healthmaster"
		}
	if stri=="medicine.availability":
		result = req.get("result")
		parameters = result.get("parameters")
		zone = parameters.get("medicines")
		speech = "The medicine details will be updated soon"
		print("Response:")
		print(speech)
		return {
			"speech" : speech,
			"displayText": speech,
			"source": "Healthmaster"
		}
	if stri=="doctor.speciality":
		result = req.get("result")
		parameters = result.get("parameters")
		location = str(parameters.get("locations"))
		dictionary = {"mangalore" : 1, "panaji" : 2, "jaipur" : 3, "salem" : 4, "vijayawada" : 5}
		if location in dictionary.keys():
			hid = dictionary[location.lower()]
		else:
			hid = "*"
		speciality = str(parameters.get("Doc_type"))
		if speciality is None:
			speciality = "*"
		
		conn = sqlite3.connect('hospital.db')
		cursor = conn.execute("SELECT DNAME, DFEE FROM DOCTOR WHERE HID = " + str(hid) +" AND DSPECIAL = \"" + speciality + "\"")
		data = cursor.fetchall()
		if len(data) == 0:
			speech = "No doctors available for the given input."
		else:
			speech = "#\tDoctor Name\t\tFee\n" +  "\n"
			i=1
			for name, fee in data:
				speech = speech + str(i) + "\t" + name + "\t" + str(fee) + "\n"
				i+=1
		print("Response:")
		print(speech)
		return {
			"speech" : speech,
			"displayText": speech,
			"source": "Healthmaster"
		}
	
	else:
		return {
			"speech" : "Try again",
			"displayText": "Try again",
			"source": "Healthmaster"
		}


if __name__ == '__main__':
    app.run(debug=True)#,ssl_context='adhoc')
	