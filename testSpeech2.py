import pyoxford
from tokens import *

text = "hello are you come from Chicago and have one thousand U.S. dollars per month"
api = pyoxford.speech("kage-test-speech", oxford_computer_speech)

# text to speech (.wav file)
binary = api.text_to_speech(text)
with open("voice.wav", "wb") as f:
    f.write(binary)

# speech to text
recognized = api.speech_to_text("voice.wav")
print(recognized)

if text == recognized:
    print(recognized)
    print("success!!")