from flask import Flask, render_template, Response, request, url_for, redirect
from camerabridge import camerabridge
from flask import jsonify
from flask import g, flash
import json

camerabridge = camerabridge()

def create_app():
    app = Flask(__name__)
    return app

app = create_app()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Mjpeg flask demo')

def gen(camera):
    while True:
        frame = camera.get_frame()
        content_length = len(frame)
        if content_length > 0:
           yield ('--frame\r\n')
           yield ('Content-Type:image/jpeg\r\n')
           yield('Content-Length:' +  str(content_length) + '\r\n')
           yield ('\r\n')
           yield (frame)
           yield ('\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(camerabridge), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(threaded=True, debug=True, host='0.0.0.0', port=5001, use_reloader=False)
