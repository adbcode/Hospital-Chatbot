from flask import *
import json,requests,sys
import apiai

app = Flask(__name__)

CLIENT_ACCESS_TOKEN = 'c0dce7652e6b4a16b3e818ff84b78373'

ai= apiai.ApiAI(CLIENT_ACCESS_TOKEN)

@app.route('/')
def Main():
    return render_template("homepage.html")


if __name__ == '__main__':
    app.run(debug=True,ssl_context='adhoc')
	