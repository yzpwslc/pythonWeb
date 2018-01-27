from flask import Flask
import RPi.GPIO as gpio
import time

class rasCointrol(object):
	def __init__(self):
		self.lPins = [17,18,23]
		self.cStates = [0,0,0]
		self.cStates1 = [1,1,1]
		gpio.setmode(gpio.BCM)
		[gpio.setup(self.lPins[i],gpio.OUT) for i in range(len(self.lPins))]
		[gpio.output(self.lPins[i],v) for i,v in enumerate(self.cStates)]
		time.sleep(1)
	def __del__(self):
		gpio.clenup()
		
	def ledOn(self):
		[gpio.output(self.lPins[i],v) for i,v in enumerate(self.cStates1)]
		
	def ledOff(self):
		[gpio.output(self.lPins[i],v) for i,v in enumerate(self.cStates)]

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
	rs = rasCointrol()
	rs.ledOn()	
@app.route('/led0')
def led0():
	rs = rasCointrol()	
	rs.ledOff()

if __name__ == '__main__':
	app.run(host = '0.0.0.0',debug = True,port = 8000)
