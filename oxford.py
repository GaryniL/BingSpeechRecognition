import httplib, urllib, base64
from tokens import *



headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': oxford_computer_vision,
}

params = urllib.urlencode({
    # Request parameters
    'width': '100',
    'height': '100',
    'smartCropping': 'true',
})

url = urllib.urlencode({
    #body url
    "Url": "https://upload.wikimedia.org/wikipedia/commons/5/5d/RedRoo.JPG",
})

try:
    conn = httplib.HTTPSConnection('api.projectoxford.ai')
    conn.request("POST", "/vision/v1/thumbnails&%s" % params, url, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

