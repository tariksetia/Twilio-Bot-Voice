import time,sys,os
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
from directline import DirectLineAPI as DL
from utils.twilio import buildTwilioResponse

app = Flask(__name__)
converations = {}


@app.route("/", methods=['GET'])
def index():
    return "Twilio-Docker-Bot"

@app.route("/answer", methods=['GET', 'POST'])
def answer_call():
    caller = request.form.get('Caller')
    bot = DL();
    converations[caller] = bot
    return str(buildTwilioResponse("Hello! welcome to NTT service desk. How may I help?"))


@app.route("/gather", methods=['POST'])
def gather():
    user_speech = request.form.get('SpeechResult')
    caller = request.form.get('Caller')
    bot = converations[caller]
    bot._lastAccessed = time.time()
    bot.send(user_speech)
    print(caller + ': ' + user_speech)
    loop = time.time()
    msg = ""
    time.sleep(1)
    msg = bot.get()
    if not msg:
        while time.time() - loop < 60:
            try:
                msg = bot.get()
                print(msg)
                if msg :
                    break
            except Exception as e:
                print (str(e));
                pass
    bot._lastAccessed = time.time()
    print(msg)
    return str(buildTwilioResponse(msg.get('msgs'),msg.get('eoc')))

@app.route("/gather/dtmf", methods=['POST'])
def gather_dtmf():
    pass
    


if __name__ == "__main__":
    app.run('0.0.0.0', port=80, debug=True)


