# -*- coding: utf-8 -*-

'''
torstack.handler.websocket
websocket handler definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import tornado.websocket
from torstack.handler.base import BaseHandler


class WebSocketHandler(tornado.websocket.WebSocketHandler, BaseHandler):

    def initialize(self):
        super(WebSocketHandler, self).initialize()


