import http.client, urllib.parse, json, os
import xml.etree.cElementTree as ET
from tokens import *

f = open('response.xml','rb')
try:
    body = f.read();
finally:
    f.close()

all_texts = ''

tree = ET.ElementTree(ET.fromstring(body))
root = tree.getroot()
for elem in root.iter('results'):
	for elem2 in elem[0].iter('lexical'):
		all_texts += elem2.text
		all_texts += '\n'

with open('result.txt', 'w+') as file:
	file.write(all_texts)
file.close()