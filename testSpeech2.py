import pyoxford
from tokens import *

text = "a b c d e f"
api = pyoxford.speech("kage-test-speech", oxford_computer_speech)

# text to speech (.wav file)
binary = api.text_to_speech(text)
with open("sound1.wav", "wb") as f:
    f.write(binary)

# speech to text
recognized = api.speech_to_text("sound1.wav")
print(recognized)

if text == recognized:
    print(recognized)
    print("success!!")