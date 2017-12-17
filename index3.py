import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import cv2
import time

from tornado.options import define,options
define("port",default=8000,help="run on the given port",type=int)

class videoHandler(tornado.web.RequestHandler):
	def get(self):
		ret,img = self.application.cam.read()
		if ret:
			self.set_header("Content-Type", "image/jpeg")
			self.set_header("Refresh", "1")
			self.set_header("content-transfer-encoding", "binary")
			r,i = cv2.imencode('.jpg',img)
			if r:
				self.write(bytes(i.data))
			else:
				self.write('Sorry,encode fail!')
		else:
			self.write('Sorry,get cam data failed!')	

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		greeting = self.get_argument('greeting','Hello')
		self.write(greeting + ', cam2!')
class Application(tornado.web.Application):
	def __init__(self):
		handlers=[(r"/",IndexHandler),(r"/cam",videoHandler)]
		settings = dict(debug=True,)
		self.cam = cv2.VideoCapture(0)
		tornado.web.Application.__init__(self,handlers,**settings)
	def __del__(self):
		self.cam.release()
		
if __name__ == "__main__":
	tornado.options.parse_command_line()
	app = Application()
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
