# -*- coding: utf-8 -*-

'''
torstack.handler.ajax
ajax handler definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import traceback
from torstack.handler.base import BaseHandler

class AjaxHandler(BaseHandler):

    def initialize(self):
        super(AjaxHandler, self).initialize()
        self.set_header('Content-Type', 'text/json')

    def write_error(self, status_code, **kwargs):
        self._status_code = 200

        if "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            lines = []
            for line in traceback.format_exception(*kwargs["exc_info"]):
                lines.append(line)

            self.write_json(dict(traceback=''.join(lines)), status_code, self._reason)

        else:
            self.write_json(None, status_code, self._reason)

    def write_json(self, data, status_code=200, msg='success.'):
        self.finish(dumps({
            'code': status_code,
            'msg': msg,
            'data': data
        }))

