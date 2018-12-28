# -*- coding: utf-8 -*-

'''
torstack.handler.rest
rest handler definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

from __future__ import absolute_import, unicode_literals
import sys
import json
import time
from torstack.handler.base import BaseHandler
from torstack.exception import BaseException

class MobRestHandler(BaseHandler):

    def initialize(self):
        super(MobRestHandler, self).initialize()
        self.rest = self.application.rest
        self._token = None
        self._token_data = None

        if self.config['rest']['rest_enable'] == False:
            raise BaseException('10105', 'error rest config.')

        if self.config['rest']['rest']['allow_remote_access'] == True:
            self.access_control_allow()

        self.set_header("Content-Type", "application/json; charset=UTF-8")

    def access_control_allow(self):
        # 允许 JS 跨域调用
        self.set_header("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Depth, User-Agent, X-File-Size, "
                                                        "X-Requested-With, X-Requested-By, If-Modified-Since, "
                                                        "X-File-Name, Cache-Control, Token")
        self.set_header('Access-Control-Allow-Origin', '*')

    @property
    def headers(self):
        '''
        :return: headers
        '''
        headers = dict()
        for name in self.rest.headers:
            headers[name] = self.request.headers.get(name, '')
        return headers

    def response(self, code=0, data={}, message='', **kwargs):
        '''
        rest api result
        :param code:
        :param data:
        :param message:
        :param kwargs:
        :return:
        '''
        try:
            self.response_json(code, data, message, **kwargs)
        except:
            message = str(sys.exc_info()[0])
            self.set_status(500)
            self.response_json(code=500, message=message, **kwargs)

    def response_json(self, code=0, data={}, message='success.', **kwargs):
        '''
        rest api result
        :param code:
        :param data:
        :param message:
        :param kwargs:
        :return:
        '''
        result = self.rest.response.copy()
        result.update(kwargs)
        result['code'] = code
        result['data'] = data
        result['message'] = message
        result['timestamp'] = time.time()
        self.write(json.dumps(result))
        self.finish()


