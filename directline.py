import requests
import time, os


secret = os.environ.get("DLKEY","YjyPZXsnkxk.cwA.VYw.14szPXTXn6QEeu5D15HdCQDK3kjp7BRvVkUrUmtg1Zs");

class DirectLineAPI(object):
    """Shared methods for the parsed result objects."""

    def __init__(self, user='test', direct_line_secret=secret):
        self._direct_line_secret = direct_line_secret
        self._base_url = 'https://directline.botframework.com/v3/directline'
        self._user = user
        self._set_headers()
        
        self._start_conversation()


    def _set_headers(self):
        headers = {'Content-Type': 'application/json'}
        value = ' '.join(['Bearer', self._direct_line_secret])
        headers.update({'Authorization': value})
        self._headers = headers

    def _start_conversation(self):
        # For Generating a token use
        # url = '/'.join([self._base_url, 'tokens/generate'])
        # botresponse = requests.post(url, headers=self._headers)
        # jsonresponse = botresponse.json()
        # self._token = jsonresponse['token']

        # Start conversation and get us a conversationId to use
        url = '/'.join([self._base_url, 'conversations'])
        botresponse = requests.post(url, headers=self._headers)

        # Extract the conversationID for sending messages to bot
        jsonresponse = botresponse.json()
        self._conversationid = jsonresponse['conversationId']
        self._watermark = None
        self._lastaccessed = time.time()


    def send(self, text):
        """Send raw text to bot framework using directline api"""
        url = '/'.join([self._base_url, 'conversations', self._conversationid, 'activities'])
        jsonpayload = {
            'conversationId': self._conversationid,
            'type': 'message',
            'from': {'id': self._user},
            'text': text
        }
        botresponse = requests.post(url, headers=self._headers, json=jsonpayload)
        if botresponse.status_code == 200:
            return "message sent"
        return "error contacting bot"

    def get(self):
        """Get a response message back from the botframework using directline api"""
        url = '/'.join([self._base_url, 'conversations', self._conversationid, 'activities'])
        url = url + '?watermark=' + str(self._watermark) if self._watermark else url
        resp = requests.get(url, headers=self._headers,
                                   json={'conversationId': self._conversationid})

        
        if resp.status_code == 200 and len(resp.json()['activities']):
            res = resp.json()
            self._watermark = res['watermark']
            activities = res['activities']
            print(activities)
            botactivities = filter(lambda x: x['from']['id'] != self._user, activities)
            msgs = [activity.get('text',None) for activity in botactivities]
            msgs = filter(lambda x:x is not None, msgs)
            msgs = '. '.join(msgs)
            print(msgs)
            eoc = list(filter(lambda x: x.get('type') == 'endOfConversation', activities))
            eoc = True if eoc else False
            return {'msgs': msgs, 'eoc':eoc}
        elif not len(resp.json()['activities']):
            return None
        return "error contacting bot for response"