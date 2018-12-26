# -*- coding: utf-8 -*-

'''
torstack.handler.ajax
ajax handler definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import traceback
import json
import time
import sys
from torstack.handler.base import BaseHandler

class WebRestHandler(BaseHandler):

    def initialize(self):
        super(WebRestHandler, self).initialize()
        self.rest = self.application.rest

        if self.config['rest']['rest_enable'] == False:
            raise BaseException('10105', 'error rest config.')

        self.set_header("Content-Type", "application/json; charset=UTF-8")

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

