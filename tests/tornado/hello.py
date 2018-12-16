# -*- coding: utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

settings = {
    'debug': False,
    'port': 8888,
    'cookie_secret': '__cookie_secret__',
    'xsrf_cookies': False,
    'compress_response': True,
    'max_threads_num': 500,
    'login_url': '/login',
    'template_path': '__website/template',
    'static_path': '__website/static',
}

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user!')

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)], **settings)
    http_server = tornado.httpserver.HTTPServer(app)
    # http_server.listen(options.port)
    http_server.bind(8888)
    http_server.start(0)  # Forks multiple sub-processes
    tornado.ioloop.IOLoop.instance().start()

