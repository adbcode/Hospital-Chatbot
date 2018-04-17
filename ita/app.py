#!/usr/bin/env python
# coding:utf-8

import urllib
import json
from flask import *
import json,requests,sys
import apiai
import sqlite3
import datetime

app = Flask(__name__)

CLIENT_ACCESS_TOKEN = 'c0dce7652e6b4a16b3e818ff84b78373'

ai= apiai.ApiAI(CLIENT_ACCESS_TOKEN)
conn = sqlite3.connect('hospital1.db')

@app.route('/')
def main():
	return render_template('home.html')
@app.route('/home')
def index():
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
			conn = sqlite3.connect('hospital1.db')
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
		conn = sqlite3.connect('hospital1.db')
		result = req.get("result")
		parameters = result.get("parameters")
		medicine = str(parameters.get("medicines"))
		cursor = conn.execute("SELECT MAVAIL FROM MEDICINE WHERE MNAME = \"" + medicine + "\"")
		data = cursor.fetchone()
		if int(data[0]) == 1:
			speech = "The requested medicine is available."
		else:
			speech = "The requested medicine is currently unavailable."
		print("Response:")
		print(speech)
		return {
			"speech" : speech,
			"displayText": speech,
			"source": "Healthmaster"
		}
	if stri=="doctor.speciality":
		conn = sqlite3.connect('hospital1.db')
		result = req.get("result")
		parameters = result.get("parameters")
		location = str(parameters.get("locations"))
		dictionary = {"mangalore" : 1, "panaji" : 2, "jaipur" : 3, "salem" : 4, "vijayawada" : 5}
		if location in dictionary.keys():
			hid = dictionary[location.lower()]
			speciality = str(parameters.get("Doc_type"))
			cursor = conn.execute("SELECT DNAME, DFEE, DID FROM DOCTOR WHERE HID = " + str(hid) + " AND DSPECIAL = \"" + speciality + "\"")
			data = cursor.fetchall()
			if len(data) == 0:
				speech = "No doctors available for the given input."
			else: 
				#speech = "#\tDoctor Name\t\tFee\n"
				i=1
				for name, fee, did in data:
					speech =  str(i) + "-" + name + "    Fee :\t" + str(fee) + "\n"
					i+=1
					print did

		else:
			speech = "No doctors available for the given location."
		print("Response:")
		print(speech)
		conn.close()
		return {
			"speech" : speech,
			"displayText": speech,
			"source": "Healthmaster"
		}
	
	if stri=="medicine.info":
		conn = sqlite3.connect('hospital1.db')
		result = req.get("result")
		parameters = result.get("parameters")
		medicine = str(parameters.get("medicines"))
		cursor = conn.execute("SELECT MDOSAGE, MPRICE FROM MEDICINE WHERE MNAME = \"" + medicine+"\"")
		data = cursor.fetchone()
		if len(data) == 0:
			speech = "The requested medicine is not present in the records."
		else:
			speech = medicine + " is to be taken " + str(data[0]).lower() + " and costs Rs. " + str(data[1]) + "."
		print("Response:")
		print(speech)
		return {
			"speech" : speech,
			"displayText": speech,
			"source": "Healthmaster"
		}
	
	if stri=="symptom":
		conn = sqlite3.connect('hospital1.db')
		result = req.get("result")
		parameters = result.get("parameters")
		symptom = str(parameters.get("symptoms"))
		cursor = conn.execute("SELECT MNAME, MDOSAGE, MPRICE FROM MEDICINE WHERE MID = (SELECT SMED FROM SYMPTOMS WHERE SNAME = \"" + symptom.lower() + "\" LIMIT 1)")
		data = cursor.fetchone()
		if len(data) == 0:
			speech = "Sorry but I am unable to help you with this health problem. Consider consulting an appropriate doctor."
		else:
			speech = "Please take " + data[0] + " " + data[1].lower() + ". The medicine will cost Rs. " + str(data[2]) + "."
		print("Response:")
		print(speech)
		return {
			"speech" : speech,
			"displayText": speech,
			"source": "Healthmaster"
		}
	
	if stri=="Register.new":
		conn = sqlite3.connect('hospital1.db')
		result = req.get("result")
		parameters = result.get("parameters")
		name = str(parameters.get("name"))
		age = str(parameters.get("age"))
		sex = str(parameters.get("sex"))
		cursor = conn.execute("SELECT PID FROM PATIENT WHERE PNAME = \"" + name + "\" AND PAGE = " + age + " AND PSEX = \"" + sex + "\"")
		data = cursor.fetchall()
		if len(data) == 0:
			cursor = conn.execute("INSERT INTO PATIENT (PNAME, PAGE, PSEX) VALUES (\'" + name + "\', " + age + ", \'" + sex + "\')")
			cursor = conn.execute("SELECT PID FROM PATIENT WHERE PNAME = \"" + name + "\" AND PAGE = " + age + " AND PSEX = \"" + sex + "\"")
			data = cursor.fetchone()
			speech = "New patient profile created. Your patient id is: " + str(data[0]) + "."
		else: 
			speech = "Profile already exists. Your patient id is: " + str(data[0][0]) + "."
		print("Response:")
		print(speech)
		conn.commit()
		conn.close()
		return {
			"speech" : speech,
			"displayText": speech,
			"source": "Healthmaster"
		}
	
	if stri=="appointment.book":
		conn = sqlite3.connect('hospital1.db')
		result = req.get("result")
		parameters = result.get("parameters")
		pid = str(parameters.get("pid"))
		time = str(parameters.get("time"))
		date = str(parameters.get("date"))
		did = str(parameters.get("did"))
		purpose = str(parameters.get("purpose"))
		location = str(parameters.get("location"))
		
		dictionary = {"mangalore" : 1, "panaji" : 2, "jaipur" : 3, "salem" : 4, "vijayawada" : 5}
		
		if location in dictionary.keys():
			hid = str(dictionary[location.lower()])
			cursor = conn.execute("SELECT * FROM DOCTOR WHERE DID = " + did + " AND HID = " + hid)
			data = cursor.fetchall()
			
			if len(data) != 0:
				cursor = conn.execute("SELECT * FROM PATIENT WHERE PID = " + pid)
				data = cursor.fetchall()
				
				if len(data) != 0:
					DateTime = date + " " + time
					cursor = conn.execute("SELECT PID FROM APPOINTMENT WHERE DID = " + did + " AND ADATETIME = \"" + DateTime + "\" AND HID = " + hid)
					data = cursor.fetchall()
					
					if len(data) != 0:
						if pid in data:
							speech = "Your appointment is already booked for the given time and doctor."
						else:
							speech = "The requested doctor already has appointment in the given time. Please book for another time."
					
					else:
						m = datetime.datetime.strptime(date,'%Y-%m-%d').strftime('%A')
						cursor = conn.execute("SELECT TIME FROM AVAILABLE WHERE WEEKDAY = \""+m+"\"")
						time_variable = cursor.fetchone()[0]
						time_variable= str(time_variable)				
						time1, time2 = time_variable.split("-")
						time1=str(time1)
						print time1
						timeA = datetime.datetime.strptime(time1, "%H:%M:%S")
						timeB = datetime.datetime.strptime(time2, "%H:%M:%S")
						timeC = datetime.datetime.strptime(time, "%H:%M:%S")
						if timeC >timeA and timeC < timeB:
							cursor = conn.execute("INSERT INTO APPOINTMENT(PID, DID, HID, PURPOSE, ADATETIME, AFEE) VALUES(" + pid + ", " + did + ", " + hid + ", \"" + purpose + "\", \"" + DateTime + "\", 0)")
							speech = "Your appointment is booked at "+ time +" on "+ date
						else:
							speech = "The requested doctor is unavailable at the requested time. Please book for another time."
				else:
					speech="The patient does not exist in the records. Please try again or register before booking an appointment."
			else:
				speech = "The doctor does not exist in the records and/or the doctor does not work in the given hospital. Please try again."
		else:
			speech = "The location does not exist in the records. Please try again."
						
		print("Response:")
		print(speech)
		conn.commit()
		conn.close()
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
	