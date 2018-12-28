# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import tornado.web
from tornado import gen
from torstack.handler.mobrest import MobRestHandler
import uuid

class RestfulHandler(MobRestHandler):
    '''
    RestfulHandler
    '''
    def initialize(self):
        super(RestfulHandler, self).initialize()
        self.dbname = 'test'
        self.db = self.storage['sync_mysql']


class InitHandler(RestfulHandler):
    '''
    initialize
    '''
    @gen.coroutine
    def get(self):
        result = self.headers
        # result = None
        return self.response(code=0, data=result, message=u'操作成功', uuid=str(uuid.uuid4()))

class ErrorHandler(MobRestHandler):
    '''
    error handler
    '''
    @gen.coroutine
    def prepare(self):
        return self.response(code=500, message='uri not found')