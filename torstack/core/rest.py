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

    HEADER_CONFIG = dict(
        token='',
        version='',
        signature='',
        timestamp='',
    )

    RESPONSE_CONFIG = dict(
        code='200',
        data='',
        message='',
        timestamp='',
    )


    def __init__(self, driver, config={}):
        self.__init_config(config)
        self.__init_driver(driver)

    def __init_config(self, config={}):
        '''
        Init rest configurations.
        :param self:
        :param config:
        :return:
        '''
        rest_config = dict(
            enable=config['rest_enable'],
            allow_remote_access=config['allow_remote_access'],
            token_prefix=config['token_prefix'],
            token_lifetime=config['token_lifetime'],
        )
        header_config = config['rest_header']
        response_config = config['rest_response']
        if config:
            self.REST_CONFIG.update(rest_config)
        if header_config:
            self.HEADER_CONFIG.update(header_config)
        if response_config:
            self.RESPONSE_CONFIG.update(response_config)

    def __init_driver(self, driver):
        '''
        setup rest driver.
        :return:
        '''
        if driver:
            self.driver = driver
        else:
            from torstack.storage.file import FileStorage
            self.driver = FileStorage()

    def _generate_token(self, blength=36):
        '''
        generate token
        :param blength:
        :return:
        '''
        return EncipherLibrary.gen_token(blength)

    def get(self, key, default=None):
        '''
        Return token value with name as key.
        :param key:
        :param default:
        :return:
        '''
        value = self.driver.get(key)
        if value:
            if isinstance(value, str):
                return value
            else:
                return value.decode('utf-8')
        else:
            return default

    def set(self, key, value):
        '''
        Add/Update token value
        :param key:
        :param value:
        :return:
        '''
        if isinstance(value, str):
            token_string = value
        elif isinstance(value, dict):
            token_string = json.dumps(value)
        elif isinstance(value, object):
            token_string = json.dumps(value.__dict__)
        else:
            raise BaseException('10001', 'error data format: %s.' % str(value))

        self.driver.save(key, token_string, self.REST_CONFIG['lifetime'])

    def delete(self, key):
        '''
        Delete token key-value pair
        :param key:
        :return:
        '''
        return self.driver.delete(key)

    def new_token(self):
        '''
        :return: new token
        '''
        return self._generate_token(36)

    @property
    def headers(self):
        return self.HEADER_CONFIG

    @property
    def response(self):
        return self.RESPONSE_CONFIG