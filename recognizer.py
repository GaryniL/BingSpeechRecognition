import http.client, urllib.parse, json, os, sys
import wave,csv,time
import contextlib
import xml.etree.cElementTree as ET
from tokens import *

#thanks for the sample: https://social.msdn.microsoft.com/Forums/sqlserver/en-US/138ad8a0-6e61-4929-84b4-0336290652d6/mvp-how-to-use-project-oxford-voice-recognition-api-rest-with-python?forum=mlapi
#Note: Sign up at http://www.projectoxford.ai to get a subscription key.
#Search for Speech APIs from Azure Marketplace.
#Use the subscription key as Client secret below.
clientId = "kage-test-speech"
clientSecret = oxford_speech_api
ttsHost = "https://speech.platform.bing.com"
all_strings = ''
all_data = []

def export_csv(csvdata, file_name):
	f = open(file_name, "w")
	w = csv.writer(f, lineterminator = '\n')
	for item in csvdata:
		w.writerow(item)
	f.close()

class prettyfloat(float):
    def __repr__(self):
        return "%0.2f" % self

def extract_lexical(text_body):
	# print (text_body)
	tree = ET.ElementTree(ET.fromstring(text_body))
	root = tree.getroot()
	for elem in root.iter('results'):
		for elem2 in elem[0].iter('lexical'):
			return elem2.text + '\n'

def calWavDuration(wav_path):
	with contextlib.closing(wave.open(wav_path,'r')) as wf:
	    frames = wf.getnframes()
	    rate = wf.getframerate()
	    duration = frames / float(rate)
	    return duration

def get_response(body, headers):
	#Connect to server to recognize the wave binary
	conn = http.client.HTTPSConnection("speech.platform.bing.com")
	conn.request("POST", "/recognize/query?scenarios=ulm&appid=D4D52672-91D7-4C74-8AD8-42B1D98141A5&locale=en-US&device.os=wp7&version=3.0&format=xml&requestid=1d4b6030-9099-11e0-91e4-0800200c9a66&instanceid=1d4b6030-9099-11e0-91e4-0800200c9a66", body, headers)
	response = conn.getresponse()
	print('\t',response.status, response.reason, end="\t")
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
	if response.status != 200 :
		print('[Token] ',response.status, response.reason)

	data = response.read()
	conn.close()
	accesstoken = data.decode("UTF-8")
	# print ("Oxford Access Token: " + accesstoken)

	#decode the object from json
	ddata=json.loads(accesstoken)
	access_token = ddata['access_token']
	return access_token

def send_request(body):
	headers = {"Content-type": "audio/wav; samplerate=8000",
				"Authorization": "Bearer " + access_token}
	response = get_response(body, headers)
	response_data = response.read()
	if response.status is 200:
		returnStr = extract_lexical(response_data)
	else:
		returnStr = (sound + ' ERROR!!! '+ str(response.status))
	return (returnStr,response.status)

# Read the binary from wave file
#gary's poo
workPath = os.getcwd() # get current work space
arg1 = ''
if len(sys.argv) >= 2 :
	workPath += "/" + sys.argv[1] # append data folder
	arg1 = sys.argv[1]

sound_list = os.listdir(workPath) # list all sound in folder
index = 0



audio_offset = 0.0
elapsed_total_time = 31.0 # for first time used
access_token = ''

print('Filename\tClip duration\tRequest Status\tElapsed time')
all_data.append(['Filename','duration','start','end','Speech'])
for sound in sound_list: # run through all sound
	if sound == '.DS_Store' :
		continue

	if sound.lower().endswith(('.wav')) == False:
		all_data.append([sound,'Error format'])
		continue
	
	if (elapsed_total_time / 30) >= 1 :
		# Get access token
		print('========= ','Token Renew' ,' =========')
		access_token = ''
		access_token = get_token()
		elapsed_total_time = 0.0

	elapsed_start = time.time()
	sound_output_arr = []

	print(sound, end="\t") # print sound name
	sound_output_arr.append(sound)

	duration = calWavDuration(workPath + '/' + sound)
	print("%0.2f" % duration, end="\t")# print sound duration
	sound_output_arr.append("%0.2f" % duration)
	start_time = audio_offset
	end_time = audio_offset = start_time + duration
	sound_output_arr.append("%0.2f" % start_time)
	sound_output_arr.append("%0.2f" % end_time)
	index += 1
	
	# Open audio to read
	f = open(workPath + '/' + sound,'rb')
	try:
	    body = f.read();
	finally:
	    f.close()
	speechStr, status_code = send_request(body)
	print(status_code)
	if (status_code == 200) == False:
		print('========= ','Token Renew' ,' =========')
		access_token = ''
		access_token = get_token()
		elapsed_total_time = 0.0
	sound_output_arr.append(speechStr)
	elapsed_end = time.time()
	elapsed_total_time = elapsed_total_time + (elapsed_end - elapsed_start) 
	print ('\t',"%0.2f" % elapsed_total_time)
	all_data.append(sound_output_arr)
export_csv(all_data,arg1+'.csv')
# with open('./' + arg1 + '/' + arg1 + '.txt', 'w+') as file:
# 	file.write(all_strings)
# file.close()