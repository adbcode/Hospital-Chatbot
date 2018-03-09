import sys, json, requests
from flask import Flask, request

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

app = Flask(__name__)

CLIENT_ACCESS_TOKEN = 'c0dce7652e6b4a16b3e818ff84b78373'
PAGE_ACCESS_TOKEN = 'INSERT_FACEBOOK_PAT'
VERIFY_TOKEN = 'INSERT_TOKEN'

ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def print_signage():
    return "Conversational Chatbot Webservice, send your data towards this/webhook!"

@app.route('/webhook', methods=['GET'])
def handle_verification():
    print("Handling Verification.")
    if (request.args.get('hub.verify_token', '') == VERIFY_TOKEN):
        print("Webhook verified!")
        return request.args.get('hub.challenge', '')
    else:
        print("Wrong verification token!")
        return "Error, wrong validation token"


@app.route('/webhook', methods=['POST'])
def handle_message():
    data = request.get_json()

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):  

                    sender_id = messaging_event["sender"]["id"]        
                    recipient_id = messaging_event["recipient"]["id"]  
                    message_text = messaging_event["message"]["text"]  
                    send_message_staggered(sender_id, parse_natural_text(message_text)) 


    return "ok"


def send_message(sender_id, message_text):
    r = requests.post("https://127.0.0.1:5000/",

        params={"access_token": PAGE_ACCESS_TOKEN},

        headers={"Content-Type": "application/json"}, 

        data=json.dumps({
        "recipient": {"id": sender_id},
        "message": {"text": message_text}
    }))

def parse_natural_text(user_text):
    
    request = ai.text_request()
    request.query = user_text

    response = json.loads(request.getresponse().read().decode('utf-8'))
    responseStatus = response['status']['code']
    if (responseStatus == 200):
        return (response['result']['fulfillment']['speech'])

    else:
        return ("Sorry, I couldn't understand that question")

def send_message_staggered(sender_id, message_text):

    sentenceDelimiter = ". "
    messages = message_text.split(sentenceDelimiter)
    
    for message in messages:
        send_message(sender_id, message)