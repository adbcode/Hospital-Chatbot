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
	print "Request:"
	print json.dumps(req, indent=4)
	res = makeWebhookResult(req)
	res = json.dumps(res, indent=4)
	print res
	r = make_response(res)
	r.headers['Content-Type'] = 'application/json'
	return r


def makeWebhookResult(req):
	stri = req.get("result").get("action")
	
	# Query hospital location, contact details
	if stri=="places":
		conn = sqlite3.connect('hospital.db')
		result = req.get("result")
		parameters = result.get("parameters")
		location = str(parameters.get("locations"))
		if location in dictionary.keys():
			dictionary = {"mangalore" : 1, "panaji" : 2, "jaipur" : 3, "salem" : 4, "vijayawada" : 5}
			hid = dictionary[location.lower()]
			cursor = conn.execute("SELECT HLOCATION, HPHONE FROM HOSPITAL WHERE HID = " + str(hid))
			data = cursor.fetchone()
			speech = "Hospital is located at: " + data[0] + "\nContact Details: " + str(data[1])
		else:
			speech = "There is no hospital in the given location."
		print("Response:")
		print(speech)
		conn.close()
		return {
			"speech" : speech,
			"displayText": speech,
			"source": "Healthmaster"
		}
		
	# Getting list of doctors of given specialty in a certain hospital
	if stri=="doctor.speciality":
		conn = sqlite3.connect('hospital.db')
		result = req.get("result")
		parameters = result.get("parameters")
		location = str(parameters.get("locations"))
		dictionary = {"mangalore" : 1, "panaji" : 2, "jaipur" : 3, "salem" : 4, "vijayawada" : 5}
		if location in dictionary.keys():
			hid = dictionary[location.lower()]
			speciality = str(parameters.get("Doc_type"))
			cursor = conn.execute("SELECT DNAME, DFEE FROM DOCTOR WHERE HID = " + str(hid) + " AND DSPECIAL = \"" + speciality + "\"")
			data = cursor.fetchall()
			if len(data) == 0:
				speech = "No doctors available for the given input."
			else: 
				speech = "#\tDoctor Name\t\tFee\n"
				i=1
				for name, fee in data:
					speech = speech + str(i) + "\t" + name + "\t" + str(fee) + "\n"
					i+=1

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
	
	# Checking for medicine availability
	if stri=="medicine.availability":
		conn = sqlite3.connect('hospital.db')
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
	
	# Medicine info
	if stri=="medicine.info":
		conn = sqlite3.connect('hospital.db')
		result = req.get("result")
		parameters = result.get("parameters")
		medicine = str(parameters.get("medicines"))
		cursor = conn.execute("SELECT MDOSAGE, MPRICE FROM MEDICINE WHERE MNAME = \"" + medicine + "\"")
		data = cursor.fetchone()
		if len(data) == 0:
			speech = "The requested medicine is not present in the records."
		else:
			speech = medicine + " is to be taken " + data[0].lower() + " and costs Rs. " + str(data[1]) + "."
		print("Response:")
		print(speech)
		return {
			"speech" : speech,
			"displayText": speech,
			"source": "Healthmaster"
		}
		
	# Basic health help
	if stri=="symptom":
		conn = sqlite3.connect('hospital.db')
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
	
	# Creating a new patient profile
	if stri=="patient.new":
		conn = sqlite3.connect('hospital.db')
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
	
	else:
		return {
			"speech" : "Try again",
			"displayText": "Try again",
			"source": "Healthmaster"
		}

if __name__ == '__main__':
    app.run(debug=True)#,ssl_context='adhoc')
	

# Booking appointments
#def book(data):
	# Assuming data contains 
	# PID, DID, HID, PURPOSE, ADATETIME, AFEE
	# in that order
#	return "INSERT INTO APPOINTMENT(PID, DID, HID, PURPOSE, ADATETIME, AFEE) \
#		VALUES (%s, %s, %s, %s, %s, %s)", (data[0], data[1], data[2], data[3], data[4], data[5]))

# Get a doctor's schedule
#def doctor_schedule(data):
	# Assuming data contains
	# DID
#	return "SELECT WEEKDAY, TIME FROM DOCTOR WHERE DID = %s", (data[0])