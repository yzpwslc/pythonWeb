from flask import Flask, render_template,Response
from werkzeug.datastructures import Headers
import cv2
import time
class MyResponse(Response):
    def __init__(self, response=None, **kwargs):
        kwargs['headers'] = ''
        headers = kwargs.get('headers')
        origin = ('Access-Control-Allow-Origin', '*')
        methods = ('Access-Control-Allow-Methods', 'HEAD, OPTIONS, GET, POST, DELETE, PUT')
        if headers:
            headers.add(*origin)
            headers.add(*methods)
        else:
            headers = Headers([origin, methods])
        kwargs['headers'] = headers
        return super().__init__(response, **kwargs)
		
class VideoCam(object):
	def __init__(self):
		self.video = cv2.VideoCapture(0)

	def __del__(self):
		self.video.release()

	def get_frame(self):
		success,image = self.video.read()
		ret,jpeg = cv2.imencode('.jpg',image)
		return jpeg.tobytes()

app = Flask(__name__)
app.response_class = MyResponse

@app.route('/')
def index():
	return render_template('index2.html')

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield(b'--frame\r\n'
			b'COntent-Type:image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
	return Response(gen(VideoCam()),mimetype = 'multipart/x-mixed-replace;boundary=frame')


if __name__ == '__main__':
	app.run(host = '0.0.0.0',debug = True,port = 80)
