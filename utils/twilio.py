from twilio.twiml.voice_response import VoiceResponse,Gather

def buildTwilioResponse (text, eoc=False, language='en-IN'):
    resp = VoiceResponse()
    resp.say(text, voice='alice')
    print("bot: " + text)
    if eoc:
        resp.say("Thanks for using NTT Serice Desk, Now you will be routed to Main Meu")
        resp.redirect('/answer', method='POST');
        return resp

    gather = Gather(input="speech", method="POST", action="/gather", language=language, speechTimeout='auto')
    resp.append(gather)
    resp.say("I didn't quite catch that. Please try again.", voice='alice')
    gather = Gather(input="speech", method="POST", action="/gather", language=language, speechTimeout='auto')
    resp.append(gather)
    resp.say("Disconnecting. Please try again later")
    resp.hangup()
    return resp
