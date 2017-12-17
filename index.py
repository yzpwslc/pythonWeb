from flask import Flask, render_template,Response
import RPi.GPIO as gpio
import cv2
import time

class rasCointrol(object):
	def __init__(self):
		lPins = [17,18,23]
		cStates = [0,0,0]
		cStates1 = [1,1,1]
		gpio.setmode(gpio.BCM)
		[gpio.setup(lPins[i],gpio.OUT) for i in range(len(lPins))]
		[gpio.output(lPins[i],v) for i,v in enumerate(cStates)]
		time.sleep(1)
		[gpio.output(lPins[i],v) for i,v in enumerate(cStates1)]
	def __del__(self):
		gpio.clenup()



class VideoCam(object):
	def __init__(self):
		self.video = cv2.VideoCapture(0)

	def __del__(self):
		self.video.release()

	def get_frame(self):
		success,image = self.video.read()
		ret,jpeg = cv2.imencode('.jpg',image)
		return jpeg.tobytes()

##class motorControl(object):
##	def __init__(self):
##		GPIO.setmode(GPIO.BCM)
##		self.lf_pin = 18
##		GPIO.setmode(self.lf_pin,GPIO.OUT)
##
##	def __del__(self):
##		GPIO.clenup()
##
##	def  motorStart():
##		GPIO.output(self.lf_pin,GPIO.HIGH)
##		time.sleep(10)


app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield(b'--frame\r\n'
			b'COntent-Type:image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

##def motorContor(motor):
##	motor.motorStart()
##
##@app.route('/motor_control')
##def motor_control():
##	motorContor(motorControl())
@app.route('/led')
def led():
	return Response(rasCointrol())
@app.route('/video_feed')
def video_feed():
	return Response(gen(VideoCam()),mimetype = 'multipart/x-mixed-replace;boundary=frame')


if __name__ == '__main__':
	app.run(host = '0.0.0.0',debug = True,port = 80)
