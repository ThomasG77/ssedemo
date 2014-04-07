#!/usr/bin/env python

import random
import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()

from flask import Flask, request, Response, render_template

app = Flask(__name__)

def event_stream():
    count = 0
    while True:
        x = random.uniform(-180, 180)
        y = random.uniform(-90, 90)
        gevent.sleep(5)
        yield 'retry:10000\ndata: {"type": "Feature","properties": {"name": "Coors Field","amenity": "Baseball Stadium","popupContent": "This is where the Rockies play!"},"geometry": {"type": "Point","coordinates": [%s, %s]}}\n\n' % (x, y)
        count += 1

@app.route('/my_event_source')
def sse_request():
    return Response(
            event_stream(),
            mimetype='text/event-stream')

@app.route('/')
def page():
    return render_template('leaflet-sse.html')

if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 8001), app)
    http_server.serve_forever()
