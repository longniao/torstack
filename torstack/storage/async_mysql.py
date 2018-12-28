# -*- coding: utf-8 -*-

'''
torstack.storage.sync_mysql
sync mysql storage definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

from __future__ import print_function

from torstack.exception import BaseException


class AsyncMysql(object):

    def __init__(self, configs=[]):
        if not configs:
            raise BaseException('10101', 'error mysql config.')

        self.current_db = None
        self.config_list = []
        self.enginePool = {}
        self.sessionPool = {}

        self.init_configs(configs)
        self.init_pool()
        self.create_pool()
        self.check_pool()
