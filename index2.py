import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import cv2
import time

from tornado.options import define,options
define("port",default=80,help="run on the given port",type=int)

class camHandler(tornado.web.RequestHandler):
	def get(self):
		ret,img = self.IndexHandler.video.read()
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
	def __init__(self):
		self.video = cv2.VideoCapture(0)
		tornado.web.Application.__init__(self, handlers, debug = True ,cookie_secret = "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o")
	def __del__(self):
		self.video.release()
	def get(self):
		greeting = self.get_argument('greeting','Hello')
		self.write(greeting + ', friendly user2!')
		
if __name__ == "__main__":
	tornado.options.parse_command_line()
	app = tornado.web.Application(handlers=[(r"/",IndexHandler),(r"/cam",camHandler)])
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
