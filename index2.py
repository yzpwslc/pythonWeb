import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import RPi.GPIO as gpio
import time

from tornado.options import define,options
define("port",default=8000,help="run on the given port",type=int)

		

class IndexHandler(tornado.web.RequestHandler):
	# def __init__(self):
		# self.video = cv2.VideoCapture(0)
	# def __del__(self):
		# self.video.release()
	def get(self):
		greeting = self.get_argument('greeting','Hello')
		self.write(greeting + ', friendly user2!')
class controlHander(tornado.web.RequestHandler):
	def initialize(self):
		self.lPins = [17,18,23]
		self.cStates = [0,0,0]
		self.cStates1 = [1,1,1]
		gpio.setmode(gpio.BCM)
		[gpio.setup(self.lPins[i],gpio.OUT) for i in range(len(self.lPins))]
		[gpio.output(self.lPins[i],v) for i,v in enumerate(self.cStates)]
		time.sleep(1)	
		self.write('init')
	def on_finish(self):
		gpio.cleanup()		
	def get(self):
		[gpio.output(self.lPins[i],v) for i,v in enumerate(self.cStates1)]
		self.write('control')
		
if __name__ == "__main__":
	tornado.options.parse_command_line()
	app = tornado.web.Application(handlers=[(r"/",IndexHandler),(r"/led1",controlHander)],template_path = os.path.join(os.path.dirname(__file__),'templates'),static_path = os.path.join(os.path.dirname(__file__), "static"),debug=True)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
