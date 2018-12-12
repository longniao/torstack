# -*- coding: utf-8 -*-

'''
torstack..tornadoredis
tornadoredis definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import tornadoredis
import tornado.httpserver
import tornado.web
import tornado.ioloop
import tornado.gen
import logging


logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger('app')

pool = tornadoredis.ConnectionPool(
        host='localhost',
        port=6379,
        max_connections=250,
        wait_for_available=True
    )


class MainHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self):
        c = tornadoredis.Client(host="127.0.0.1",port=6379)
        foo = yield tornado.gen.Task(c.get, 'foo')
        bar = yield tornado.gen.Task(c.get, 'bar')
        zar = yield tornado.gen.Task(c.get, 'zar')
        self.set_header('Content-Type', 'text/html')
        self.render("template.html", title="Simple demo", foo=foo, bar=bar, zar=zar)


@tornado.gen.coroutine
def create_test_data():
    c = tornadoredis.Client(host="127.0.0.1",port=6379)
    with c.pipeline() as pipe:
        pipe.set('foo', 'Lorem ipsum #1', 12 * 60 * 60)
        pipe.set('bar', 'Lorem ipsum #2', 12 * 60 * 60)
        pipe.set('zar', 'Lorem ipsum #3', 12 * 60 * 60)
        # pipe.execute
        yield tornado.gen.Task(pipe.execute)
    print('Test data initialization completed.')


if __name__ == '__main__':
    # Start the data initialization routine
    application = tornado.web.Application([
        (r'/', MainHandler),
    ])

    create_test_data()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    print('Demo is runing at 0.0.0.0:8888\nQuit the demo with CONTROL-C')
    tornado.ioloop.IOLoop.instance().start()