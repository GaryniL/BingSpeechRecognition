import pyoxford, sys
from tokens import *

if len(sys.argv) == 2:
	text = sys.argv[1]
	api = pyoxford.speech("kage-test-speech", oxford_computer_speech)

	# text to speech (.wav file)
	binary = api.text_to_speech(text)
	with open("synthesized.wav", "wb") as f:
	    f.write(binary)

	# speech to text
	recognized = api.speech_to_text("synthesized.wav")

	if text.lower() == recognized.lower():
	    print("Recognized : " + recognized)
	    print("The recognized string is same as your input string")
	else:
		print("Voice is synthesized, however the recognized string is not same as your input string")
		print("Input String : " + text)
		print("Recognized : " + recognized)
else:
	print("You should input the test as argument!")