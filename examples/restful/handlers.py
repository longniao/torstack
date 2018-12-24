# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import tornado.web
from tornado import gen
from torstack.handler.rest import RestHandler
from torstack.library.encipher import EncipherLibrary
from account.user_account_service import UserAccountService

class RestfulHandler(RestHandler):
    '''
    RestfulHandler
    '''
    def initialize(self):
        super(RestfulHandler, self).initialize()
        self.dbname = 'test'
        self.db = self.storage['mysql']


class InitHandler(RestfulHandler):
    '''
    initialize
    '''
    def get(self):
        result = self.headers
        result = None
        return self.response(code=0, data=result, message=u'操作成功')


class ErrorHandler(RestHandler):
    '''
    error handler
    '''
    def prepare(self):
        return self.response(code=500, message='uri not found')