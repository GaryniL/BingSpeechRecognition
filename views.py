"""
Routes and views for the flask application.
"""

from datetime import datetime
import urllib
import urllib2
import json
from tokens import *

from flask import render_template, Flask, request, make_response, abort
from FlaskWebProject import app

from bing import *

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/search/<q>/')
def search(q='kangaroo'):
    url = bing_image_return(str(q))
    thumbnailed_stream = return_oxford_thumbnail_binary(str(url)) 
    #print thumbnailed_url
    #print type(thumbnailed_stream)
    return render_template(
        'searched.html',
        title = 'Searched',
        imgurl = url,
        thumbnail = 'data:image/png;base64,' + thumbnailed_stream
    )
    
#result_list = json_result['d']['results']
#print result_list

#http://2.bp.blogspot.com/-BLYZd7ETKZQ/UPwXD8KiNrI/AAAAAAAAEMA/Ns5Z6rqYbds/s1600/Kangaroo-Facts-and-Images+06.jpg