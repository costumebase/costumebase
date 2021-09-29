import os

from twilio.rest import Client

from twilio.base.exceptions import TwilioRestException



account_sid = 'AC012310b644c16105bc87239faa65c8b7'
auth_token = '94f1013cc81ec9d4a4a10ab843282b96'

client = Client(account_sid, auth_token)


def send_sms(user_code, phone):
    try:
        message = client.messages.create(
            body=f"hi! Your verification code is {user_code}",
            from_='+18135364324',
            to=f'{phone}'
        )
    except TwilioRestException as e:
        print(e)

#     print(message.sid)


# message = client.messages.create(
#         body=f"hi! Your user and verification code is ",
#         from_='+18135364324',
#         to='+8801743568504'
#     )



# import urllib.request
# import urllib.parse


# def sendSMS(apikey, numbers, sender, message):
#     data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
#         'message' : message, 'sender': sender})
#     data = data.encode('utf-8')
#     request = urllib.request.Request("https://api.txtlocal.com/send/?")
#     f = urllib.request.urlopen(request, data)
#     fr = f.read()
#     return(fr)


# resp =  sendSMS('aplic code here blah blah, '5252589652',
#     'lol', 'testing testing')
# print ("hell no ", str(resp))

# import requests
# url = 'https://api.txtlocal.com/send/?'

# params = {'username':'kevinmatthews013@gmail.com',
#           'apiKey':'NDVhOGY4NjViNTcxMjA0OTk0ZjU2ODRkMDBkNmY1MTk='
#          }

# def check_balance(url):
#     url = url+'balance'
#     response = requests.get(url,params=params)
#     return response.json()

# def send_sms(url,params):
#     url = url
#     print(url)
#     #Phone numbers inside braces {} in commas
#     numbers={'991111144444'}
#     message = {'Hi, This is a Sample message'}
#     params['numbers'] = numbers
#     params['message'] = message
#     response = requests.post(url,params=params)
#     return response.json()

# resp =  send_sms(url, params)

# print ("hell  ", str(resp))

# print(url)


# def inbox(url):
#     url = url+'get_inboxes'
#     response = requests.get(url,params=params)
#     return response.json()