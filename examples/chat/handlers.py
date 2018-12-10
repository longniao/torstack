# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import tornado.web
from tornado import gen
from torstack.handler.base import BaseHandler
from torstack.library.encipher import EncipherLibrary
from user_account_service import UserAccountService

class HomeHandler(BaseHandler):
    '''
    home
    '''
    @tornado.web.authenticated
    def get(self):
        messages = self.read_messages()
        return self.render("account/home.html", messages=messages)

