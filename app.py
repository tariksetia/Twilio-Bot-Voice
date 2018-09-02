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
    bot = DL(caller);
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
        while time.time() - loop <= 12:
            try:
                msg = bot.get()
                print(msg)
                if msg :
                    break
                time.sleep(.5)
            except Exception as e:
                print (str(e));
                pass
    bot._lastAccessed = time.time()
    print(msg)
    return str(buildTwilioResponse(msg.get('msgs'), msg.get('endOfConversation'), msg.get('waitForResponse'), msg.get('routeToMainMenu'), hangUp=msg.get('hangUp') ))

@app.route("/gather/dtmf", methods=['POST'])
def gather_dtmf():
    pass

@app.route("/realtimevoice", methods=['get'])
def realTimeVoice():
    print(request.values);
    return str(request.values)

@app.route('/wait/<ntry>', methods=['POST'])
def waitForBotRespsonse(ntry=1):
    caller = request.form.get('Caller')
    bot = converations[caller]
    if (int(ntry)>7):
        return str(buildTwilioResponse('Sorry I could not reply from the application', routeToMainMenu=True))
    msg = bot.get()
    bot._lastAccessed = time.time()
    loop = time.time()
    if not msg:
        while time.time() - loop <= 10:
            try:
                msg=bot.get()
                if msg:
                    break
                time.sleep(2)
            except Exception as e:
                print(str(e))
                pass
    bot._lastAccessed = time.time()
    if not msg:
        resp = VoiceResponse()
        url = '/wait/' + str(int(ntry)+1)
        resp.redirect(url, method='POST');
        return str(resp)
    else:
        return str(buildTwilioResponse(msg.get('msgs'), msg.get('endOfConversation'), msg.get('waitForResponse'), msg.get('routeToMainMenu'), hangUp=msg.get('hangUp')))

           


if __name__ == "__main__":
    app.run('0.0.0.0', port=80,debug=True)


