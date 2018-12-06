# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import tornado.web
from torstack.handler.base import BaseHandler

class AccountHandler(BaseHandler):

    def initialize(self):
        super(AccountHandler, self).initialize()
        self.dbname = 'test'
        self.db = self.settings['_storage_mysql']


