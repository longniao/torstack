# -*- coding: utf-8 -*-

'''
torstack.uimodule.user_message
user_message uimodule definition.

:copyright: (c) 2019 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import tornado.web
from tornado.log import app_log


class user_message(tornado.web.UIModule):
    '''
    read user message
    '''

    def render(self):
        try:
            message = self.handler.read_messages()
        except Exception as ex:
            app_log.exception(ex)

