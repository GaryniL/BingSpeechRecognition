import http.client, urllib.parse, json, os, sys, wave, csv, time, contextlib
import xml.etree.cElementTree as ET
from tokens import *
from configs import *

clientId = "kage-test-speech"
clientSecret = oxford_speech_api
ttsHost = "https://speech.platform.bing.com"
all_strings = ''
all_data = []

def import_csv(file_name):
	f = open(file_name, 'r')  
	csv_data = list(csv.reader(f, lineterminator = '\n'))
	f.close()
	return csv_data

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
	if 'access_token' in ddata:
		access_token = ddata['access_token']
	else:
		access_token = ''
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
workPath = os.getcwd() # get current work space
arg1 = ''
if len(sys.argv) >= 2 :
	workPath += "/" + sys.argv[1] # append data folder
	arg1 = sys.argv[1]

# determine fast or slow mode
arg2 = 1
if len(sys.argv) >= 3 :
	if sys.argv[2].lower() == 'slow' :
		print('[Slow mode]')
		arg2 = 0
	else :
		print('[Fast mode]')
		arg2 = 1

sound_list = os.listdir(workPath) # list all sound in folder

audio_offset = 0.0
elapsed_total_time = token_renew_time+1 # for first time used
access_token = ''

if os.path.exists(arg1+'.csv'):
	csv_data = import_csv(arg1+'.csv')



print('Filename\tClip duration\tRequest Status\tElapsed time')
all_data.append(['Filename','duration','start','end','Status','Speech'])

index = 0
for sound in sound_list: # run through all sound
	if sound == '.DS_Store' :
		continue

	if sound.lower().endswith(('.wav')) == False:
		all_data.append([sound,'Wrong voice file format'])
		continue
	this_status = 0
	index = index + 1

	# Check CSV if this file already process
	if 'csv_data' in globals():
		this_prev_data = csv_data[index]
		if this_prev_data[4] == '1' :
			# success process before
			print(this_prev_data[0],'\t',this_prev_data[1],'\t\t','OK','\t\t','skip')
			audio_offset = float(this_prev_data[3])
			# sound_output_arr.append(this_prev_data[0]) # file name
			# sound_output_arr.append(this_prev_data[1]) # duration
			# sound_output_arr.append(this_prev_data[2]) # start_time
			# sound_output_arr.append(this_prev_data[3]) # end_time
			# sound_output_arr.append(this_prev_data[4]) # this_status
			all_data.append(this_prev_data)
			continue


	# Fast mode / renew token 30 sec
	if (elapsed_total_time / token_renew_time) >= 1 and arg2 == 1 :
		# Get access token
		print('========= ','Token Renew' ,' =========')
		access_token = ''
		access_token = get_token()
		elapsed_total_time = 0.0

	# Slow mode / renew token every time
	elif arg2 == 0 :
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
	
	# Open audio to read
	f = open(workPath + '/' + sound,'rb')
	try:
	    body = f.read();
	finally:
	    f.close()

	status_code = 200
	speechStr, status_code = send_request(body)
	
	if (status_code == 200) == False:
		for i in range(retryTimes):
			print('[Token]', str(i), end=" ")
			access_token = ''
			access_token = get_token()
			elapsed_total_time = 0.0
			speechStr, status_code = send_request(body)

	# Check success or not
	if status_code == 200 :
		this_status = 1
	else :
		this_status = 0

	sound_output_arr.append(this_status)

	sound_output_arr.append(speechStr)
	elapsed_end = time.time()
	elapsed_total_time = elapsed_total_time + (elapsed_end - elapsed_start) 
	print ('\t',"%0.2f" % elapsed_total_time)
	all_data.append(sound_output_arr)
export_csv(all_data,arg1+'.csv')
