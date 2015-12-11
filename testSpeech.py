import http.client, urllib.parse, json, os, sys
import xml.etree.cElementTree as ET
from tokens import *

#thanks for the sample: https://social.msdn.microsoft.com/Forums/sqlserver/en-US/138ad8a0-6e61-4929-84b4-0336290652d6/mvp-how-to-use-project-oxford-voice-recognition-api-rest-with-python?forum=mlapi
#Note: Sign up at http://www.projectoxford.ai to get a subscription key.
#Search for Speech APIs from Azure Marketplace.
#Use the subscription key as Client secret below.
clientId = "kage-test-speech"
clientSecret = oxford_computer_speech
ttsHost = "https://speech.platform.bing.com"
all_strings = ''

def extract_lexical(text_body):
	# print (text_body)
	tree = ET.ElementTree(ET.fromstring(text_body))
	root = tree.getroot()
	for elem in root.iter('results'):
		for elem2 in elem[0].iter('lexical'):
			return elem2.text + '\n'

def get_response(body, headers):
	#Connect to server to recognize the wave binary
	conn = http.client.HTTPSConnection("speech.platform.bing.com")
	conn.request("POST", "/recognize/query?scenarios=ulm&appid=D4D52672-91D7-4C74-8AD8-42B1D98141A5&locale=en-US&device.os=wp7&version=3.0&format=xml&requestid=1d4b6030-9099-11e0-91e4-0800200c9a66&instanceid=1d4b6030-9099-11e0-91e4-0800200c9a66", body, headers)
	response = conn.getresponse()
	print(response.status, response.reason)
	# conn.close()
	return response

def get_token():
	params = urllib.parse.urlencode({'grant_type': 'client_credentials', 'client_id': clientId, 'client_secret': clientSecret, 'scope': ttsHost})
	# print ("The body data: %s" %(params))
	headers = {"Content-type": "application/x-www-form-urlencoded"}
	AccessTokenHost = "oxford-speech.cloudapp.net"
	path = "/token/issueToken"

	# Connect to server to get the Oxford Access Token
	conn = http.client.HTTPSConnection(AccessTokenHost)
	conn.request("POST", path, params, headers)
	response = conn.getresponse()
	# print(response.status, response.reason)

	data = response.read()
	conn.close()
	accesstoken = data.decode("UTF-8")
	# print ("Oxford Access Token: " + accesstoken)

	#decode the object from json
	ddata=json.loads(accesstoken)
	access_token = ddata['access_token']
	return access_token

# Read the binary from wave file
#gary's poo
workPath = os.getcwd() # get current work space
if len(sys.argv) >= 2 :
	workPath += "/" + sys.argv[1] # append data folder
else :
	workPath += "/G7_V2V" # append data folder

sound_list = os.listdir(workPath) # list all sound in folder
index = 0
for sound in sound_list: # run through all sound 
	print (sound)
	access_token = ''
	access_token = get_token()
	index += 1
	f = open(workPath + '/' + sound,'rb')
	try:
	    body = f.read();
	finally:
	    f.close()

	headers = {"Content-type": "audio/wav; samplerate=8000",
				"Authorization": "Bearer " + access_token}
	response = get_response(body, headers)
	data = response.read()
	if response.status is 200:
		all_strings += extract_lexical(data)
	else:
		all_strings += (sound + ' ERROR!!! \n')

with open('result.txt', 'w+') as file:
	file.write(all_strings)
file.close()