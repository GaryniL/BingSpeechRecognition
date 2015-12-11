# BingSpeechRecognition

---

### About
This project includes two parts: 

1. Text to Speech Conversion
2. Speech to Text Conversion

However, to help transcribing voice recording to text easier, the main propose of this project is generating a well-organized file that includes each sentence of yoru voice recording files.

### Requirements
* Python 3
* Speech API token of Microsoft Project Oxford

### Text to Speech Conversion
In this part, we use Speech API of Microsoft Project Oxford to synthesize the voice from text inputs.

You can [subscribe a free plan](https://www.projectoxford.ai/Subscription/Index?productId=/products/54f0354049c3f70a50e79b7e) of Speech APIs, which includes 5000 free API calls per month.

Usage: 
`python synthesizer.py "Never gonna give you up, never gonna let you down."` 

Output: `synthesized.wav`