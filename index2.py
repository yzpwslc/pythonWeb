import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define,options
define("port",default=8080,help="run on the given port",type=int)

class IndexHander(tornado.web.RequesttHander):
	def get(self):
		greeting = self.get_argument('greeting','Hello')
		self.write(greeting + ', friendly user!')
		
if __name__ == "__main__":
	tornado.options.parse_command_line()
	app = tornado.web.Application(handers=[(r"/",IndexHander)])
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOloop.instance().start()