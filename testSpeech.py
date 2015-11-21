import http.client, urllib.parse, json
from tokens import *

#thanks for the sample: https://social.msdn.microsoft.com/Forums/sqlserver/en-US/138ad8a0-6e61-4929-84b4-0336290652d6/mvp-how-to-use-project-oxford-voice-recognition-api-rest-with-python?forum=mlapi
#Note: Sign up at http://www.projectoxford.ai to get a subscription key.
#Search for Speech APIs from Azure Marketplace.
#Use the subscription key as Client secret below.
clientId = "kage-test-speech"
clientSecret = oxford_computer_speech
ttsHost = "https://speech.platform.bing.com"

params = urllib.parse.urlencode({'grant_type': 'client_credentials', 'client_id': clientId, 'client_secret': clientSecret, 'scope': ttsHost})

print ("The body data: %s" %(params))

headers = {"Content-type": "application/x-www-form-urlencoded"}

AccessTokenHost = "oxford-speech.cloudapp.net"
path = "/token/issueToken"

# Connect to server to get the Oxford Access Token
conn = http.client.HTTPSConnection(AccessTokenHost)
conn.request("POST", path, params, headers)
response = conn.getresponse()
print(response.status, response.reason)

data = response.read()
conn.close()
accesstoken = data.decode("UTF-8")
print ("Oxford Access Token: " + accesstoken)

#decode the object from json
ddata=json.loads(accesstoken)
access_token = ddata['access_token']

# Read the binary from wave file
f = open('sound1.wav','rb')
try:
    body = f.read();
finally:
    f.close()

headers = {"Content-type": "audio/wav; samplerate=8000",
			"Authorization": "Bearer " + access_token}

#Connect to server to recognize the wave binary
conn = http.client.HTTPSConnection("speech.platform.bing.com")
conn.request("POST", "/recognize/query?scenarios=ulm&appid=D4D52672-91D7-4C74-8AD8-42B1D98141A5&locale=en-US&device.os=wp7&version=3.0&format=xml&requestid=1d4b6030-9099-11e0-91e4-0800200c9a66&instanceid=1d4b6030-9099-11e0-91e4-0800200c9a66", body, headers)
response = conn.getresponse()
print(response.status, response.reason)
data = response.read()
print(data)
conn.close()