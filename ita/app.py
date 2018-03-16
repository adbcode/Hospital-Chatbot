import urllib
import json
from flask import *
import json,requests,sys
import apiai

app = Flask(__name__)

CLIENT_ACCESS_TOKEN = 'c0dce7652e6b4a16b3e818ff84b78373'

ai= apiai.ApiAI(CLIENT_ACCESS_TOKEN)

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
		zone = parameters.get("locations")
		speech = "The hospital place will be updated soon"
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
		zone = parameters.get("Doc_type")
		speech = "The doctors details will be updated soon"
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
	