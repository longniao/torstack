# -*- coding: utf-8 -*-

'''
torstack.core.cookie
Basic cookie definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

from __future__ import (absolute_import, division, print_function,
                        with_statement)

class CoreCookie(object):

    COOKIE_CONFIG = dict(
        enable=True,
        name='_tsid',
        expires=88473600, # 60*60*24*365*10
        expires_days=3650,
    )

    def __init__(self, config={}):
        self.__init_config(config)

    def __init_config(self, config={}):
        '''
        Init session configurations.
        :param self:
        :param config:
        :return:
        '''
        if config:
            self.COOKIE_CONFIG.update(config)

    @property
    def name(self):
        '''
        :return: cookie name
        '''
        return self.COOKIE_CONFIG['name']

    @property
    def expires(self):
        '''
        :return: expires
        '''
        return self.COOKIE_CONFIG['expires']

    @property
    def expires_days(self):
        '''
        :return: expires_days
        '''
        return self.COOKIE_CONFIG['expires_days']
