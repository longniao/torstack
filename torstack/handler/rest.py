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

class RestHandler(BaseHandler):

    def initialize(self):
        super(RestHandler, self).initialize()
        self.rest = self.application.rest
        self._token = None
        self._token_data = None

        if self.config['rest']['rest_enable'] == False:
            raise BaseException('10105', 'error rest config.')

        if self.config['rest']['allow_remote_access'] == True:
            self.access_control_allow()

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

    def response(self, **kwargs):
        '''
        response result
        :param args:
        :param kwargs:
        :return:
        '''
        try:
            result = self.rest.response.copy()
            result.update(kwargs)
            result['timestamp'] = time.time()
            self.write(json.dumps(result))
            self.finish()
        except:
            self.gen_http_error(500, "Unexpected error:", sys.exc_info()[0])

    def gen_http_error(self, status, msg):
        '''
        Generates the custom HTTP error
        :param status:
        :param msg:
        :return:
        '''
        self.clear()
        self.set_status(status)
        self.write('<html><body>' + str(msg) + '</body></html>')
        self.finish()

