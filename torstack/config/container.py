# -*- coding: utf-8 -*-

'''
torstack.config.container
config container definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''


class ConfigContainer(object):

    _CONFIG_DICT_ = dict()

    @classmethod
    def get_config(cls):
        return cls._CONFIG_DICT_

    @classmethod
    def add_mysql(cls, config):
        cls._CONFIG_DICT_['mysql'] = config

    @classmethod
    def add_redis(cls, config):
        cls._CONFIG_DICT_['redis'] = config

    @classmethod
    def add_mongodb(cls, config):
        cls._CONFIG_DICT_['mongodb'] = config

    @classmethod
    def add_memcache(cls, config):
        cls._CONFIG_DICT_['memcache'] = config

    @classmethod
    def add_application(cls, config):
        cls._CONFIG_DICT_['application'] = config

    @classmethod
    def add_session(cls, config):
        cls._CONFIG_DICT_['session'] = config

    @classmethod
    def add_cookie(cls, config):
        cls._CONFIG_DICT_['cookie'] = config

    @classmethod
    def add_log(cls, config):
        cls._CONFIG_DICT_['log'] = config

    @classmethod
    def add_base(cls, config):
        cls._CONFIG_DICT_['base'] = config

    @classmethod
    def get(cls, config):
        if config in cls._CONFIG_DICT_:
            return cls._CONFIG_DICT_[config]
        else:
            return None

    @classmethod
    def store(cls):
        define("_CONFIG_DICT_", default=cls._CONFIG_DICT_, type=dict)
