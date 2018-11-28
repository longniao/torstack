# -*- coding: utf-8 -*-

'''
torstack.core.session
Basic token definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

from torstack.core.session import CoreSession

class CoreToken(CoreSession):

    TOKEN_CONFIG = dict(
        prefix='token_',
        lifetime=315360000, # 60*60*24*365*10
    )

    def __init__(self, driver, config={}):
        self.__init_config(config)
        super(CoreToken, self).__init__(driver, self.TOKEN_CONFIG)

    def __init_config(self, config={}):
        '''
        Init session configurations.
        :param self:
        :param config:
        :return:
        '''
        if config:
            self.TOKEN_CONFIG.update(config)

