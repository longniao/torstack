# -*- coding: utf-8 -*-

'''
torstack.core.session
Basic token definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

from torstack.core.session import CoreSession

class CoreRest(object):

    REST_CONFIG = dict(
        enable=False,
        allow_remote_access=True,
        token_prefix='token_',
        token_lifetime=315360000,  # 60*60*24*365*10
    )

    REST_HEADER_CONFIG = dict(
        token='',
        version='',
        signature='',
        timestamp='',
    )

    def __init__(self, driver, config={}, header_config={}):
        self.__init_config(config, header_config)
        self.__init_session(driver)


    def __init_config(self, config={}, header_config={}):
        '''
        Init session configurations.
        :param self:
        :param config:
        :return:
        '''
        if config:
            self.REST_CONFIG.update(config)
        if header_config:
            self.REST_HEADER_CONFIG.update(header_config)


    def __init_session(self, driver):
        '''
        Init session
        :return:
        '''
        session_config = dict(
            enable=True,
        )
        session_config['prefix'] = self.REST_CONFIG['token_prefix']
        session_config['lifetime'] = self.REST_CONFIG['token_lifetime']
        self.session = CoreSession(driver, session_config)

    def get(self, key, default=None):
        return self.session.get(key, default)

    def set(self, key, value):
        self.session.save(key, value)

    def delete(self, key):
        return self.session.delete(key)

    def new_token(self):
        '''
        :return: new token
        '''
        return self.session.new_id()

    @property
    def headers(self):
        return self.REST_HEADER_CONFIG