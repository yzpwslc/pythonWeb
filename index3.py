import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import cv2
import time

from tornado.options import define,options
define("port",default=8000,help="run on the given port",type=int)

class IndexHandler(tornado.web.Application):
	def __init__(self):
		self.video = cv2.VideoCapture(0)
	def __del__(self):
		self.video.release()
		
if __name__ == "__main__":
	tornado.options.parse_command_line()
	app = IndexHandler()
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
