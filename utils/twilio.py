from twilio.twiml.voice_response import VoiceResponse,Gather,Say

def buildTwilioResponse (text, endOfConversation=False, waitForResponse=False, routeToMainMenu=False, applicationError=False, hangUp=False, language='en-US'):
    resp = VoiceResponse()
    resp.say(text, voice='Polly.Joanna')

    print("bot: " + text)
    if waitForResponse:
        print('Waiting for response from bot')
        resp.redirect('/wait/1', method="POST");
        return resp

    if routeToMainMenu:
        print('Routing to main menu')
        resp.say("Thanks for using NTT Service Desk, Now you will be routed to Main Menu", voice="Polly.Joanna")
        resp.redirect('/answer', method='POST');
        return resp
    
    if hangUp:
        print('Hanging Up event detected')
        resp.say("Thanks for using NTT Service Desk, Have a nice day. BYE!!!", voice="Polly.Joanna")
        resp.hangup()
        return str(resp)


    print('Gathering User Input')
    gather = Gather(input="speech", method="POST", action="/gather", language=language, speechTimeout='auto')
    resp.append(gather)
    resp.say("I didn't quite catch that. Please try again.", voice='Polly.Joanna')
    gather = Gather(input="speech", method="POST", action="/gather", language=language, speechTimeout='auto')
    resp.append(gather)
    resp.say("Disconnecting. Please try again later", voice='Polly.Joanna')
    resp.hangup()
    return resp

    