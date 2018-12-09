# -*- coding: utf-8 -*-

'''
torstack.config.container
config container definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

from tornado.options import define, options
from configparser import ConfigParser
import ast
from torstack.exception import BaseException

parser = ConfigParser()

class ConfigContainer(object):

    _CONFIG_DICT_ = dict()

    @classmethod
    def load_config(cls, config_file):
        parser.read(config_file, encoding='UTF-8')

    # application config ====================================

    @classmethod
    def add_settings(cls, config=None):
        if not config:
            config = ast.literal_eval(parser.get('application', 'settings'))
        cls._CONFIG_DICT_['settings'] = config

    @classmethod
    def add_log(cls, config=None):
        if not config:
            config = ast.literal_eval(parser.get('application', 'log'))
        cls._CONFIG_DICT_['log'] = config

    # base config ====================================

    @classmethod
    def add_session(cls, config=None):
        if not config:
            config = ast.literal_eval(parser.get('base', 'session'))
        cls._CONFIG_DICT_['session'] = config

    @classmethod
    def add_cookie(cls, config=None):
        if not config:
            config = ast.literal_eval(parser.get('base', 'cookie'))
        cls._CONFIG_DICT_['cookie'] = config

    # rest config ====================================

    @classmethod
    def add_rest(cls, config=None):
        if not config:
            try:
                config = ast.literal_eval(parser.get('rest', 'rest'))
            except Exception as e:
                config = None
        cls._CONFIG_DICT_['rest'] = config

    @classmethod
    def add_rest_header(cls, config=None):
        if not config:
            try:
                config = ast.literal_eval(parser.get('rest', 'rest_header'))
            except Exception as e:
                config = None
        cls._CONFIG_DICT_['rest_header'] = config

    # websocket config ====================================

    @classmethod
    def add_websocket(cls, config=None):
        if not config:
            try:
                config = ast.literal_eval(parser.get('websocket', 'websocket'))
            except Exception as e:
                config = None
        cls._CONFIG_DICT_['websocket'] = config

    # scheduler config ====================================

    @classmethod
    def add_scheduler(cls, config=None):
        if not config:
            try:
                config = ast.literal_eval(parser.get('scheduler', 'scheduler'))
            except Exception as e:
                config = None
        cls._CONFIG_DICT_['scheduler'] = config

    @classmethod
    def add_executers(cls, config=None):
        if not config:
            try:
                config = ast.literal_eval(parser.get('scheduler', 'executers'))
            except Exception as e:
                config = []
            cls._CONFIG_DICT_['executers'] = config
        else:
            if isinstance(config, list):
                cls._CONFIG_DICT_['executers'].extend(config)
            else:
                cls._CONFIG_DICT_['executers'].append(config)

    # storage config ====================================

    @classmethod
    def add_mysql(cls, config=None):
        if not config:
            try:
                config = ast.literal_eval(parser.get('storage', 'mysql'))
            except Exception as e:
                config = None
        cls._CONFIG_DICT_['mysql'] = config

    @classmethod
    def add_mongodb(cls, config=None):
        if not config:
            try:
                config = ast.literal_eval(parser.get('mongodb', 'master'))
            except Exception as e:
                config = None
        cls._CONFIG_DICT_['mongodb'] = config

    # cache config ====================================

    @classmethod
    def add_redis(cls, config=None):
        if not config:
            try:
                config = ast.literal_eval(parser.get('cache', 'redis'))
            except Exception as e:
                config = None
        cls._CONFIG_DICT_['redis'] = config

    @classmethod
    def add_memcache(cls, config=None):
        if not config:
            try:
                config = ast.literal_eval(parser.get('cache', 'memcache'))
            except Exception as e:
                config = None
        cls._CONFIG_DICT_['memcache'] = config


    @classmethod
    def get(cls, config=None, key=None):
        if not config:
            return cls._CONFIG_DICT_
        elif config not in cls._CONFIG_DICT_:
            raise BaseException('10010', 'Error config')
        else:
            item = cls._CONFIG_DICT_[config]
            if not key:
                return item
            elif key not in item:
                raise BaseException('10010', 'Error config')
            else:
                return item[key]

    @classmethod
    def set(cls, config, key, value):
        try:
            cls._CONFIG_DICT_[config][key] = value
        except Exception as e:
            raise BaseException('10010', 'Error config %s - %s - %s' % (config, key, value))


    @classmethod
    def store(cls):
        ConfigContainer.add_settings()
        ConfigContainer.add_log()
        ConfigContainer.add_session()
        ConfigContainer.add_cookie()
        ConfigContainer.add_rest()
        ConfigContainer.add_rest_header()
        ConfigContainer.add_websocket()
        ConfigContainer.add_scheduler()
        ConfigContainer.add_executers()
        ConfigContainer.add_mysql()
        ConfigContainer.add_mongodb()
        ConfigContainer.add_redis()
        ConfigContainer.add_memcache()
        define("_CONFIG_DICT_", default=cls._CONFIG_DICT_, type=dict)


    @classmethod
    def get_config(cls):
        return cls._CONFIG_DICT_
