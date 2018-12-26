# -*- coding: utf-8 -*-

'''
torstack.config.parser
config parser definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import traceback
import logging
from configparser import ConfigParser
import ast
from torstack.exception import BaseException
from torstack.config.default import *

configParser = ConfigParser()

class Parser(object):

    _dict = dict(
        application=dict(
            project_path=config_project_path,
            port=config_port,
            settings=config_settings,
            log=config_log,
        ),
        base=dict(
            session=config_session,
            cookie=config_cookie,
        ),
        rest=dict(
            rest_enable=config_rest_enable,
            allow_remote_access=config_allow_remote_access,
            token_prefix=config_token_prefix,
            token_lifetime=config_token_lifetime,
            rest_header=config_rest_header,
            rest_response=config_rest_response,
        ),
        websocket=config_websocket,
        scheduler=dict(
            scheduler=config_scheduler,
            scheduler_executers=scheduler_executers,
        ),
        storage=dict(
            mysql_enable=config_mysql_enable,
            mysql=config_mysql,
            mongodb_enable=config_mongodb_enable,
            mongodb=config_mongodb,
            redis_enable=config_redis_enable,
            redis=config_redis,
            memcache_enable=config_memcache_enable,
            memcache=config_memcache,
        ),
        elasticsearch=dict(
            elasticsearch_enable=config_elasticsearch_enable,
            elasticsearch=config_elasticsearch,
        )
    )

    def load(self, config_file=None):
        '''
        load config data from config file
        :param config_file:
        :return:
        '''
        if not config_file:
            raise BaseException('10100', 'Error config file')

        configParser.read(config_file, encoding='UTF-8')
        self.assemble()

    def parse(self, section, item):
        '''
        parse config
        :param section:
        :param item:
        :return:
        '''
        try:
            if isinstance(self._dict[section][item], dict):
                config = ast.literal_eval(configParser.get(section, item))
                self._dict[section][item].update(config)
            elif isinstance(self._dict[section][item], (list, bool)):
                config = ast.literal_eval(configParser.get(section, item))
                self._dict[section][item] = config
            else:
                config = configParser.get(section, item)
                self._dict[section][item] = config

        except Exception as e:
            # unexpected config
            config = configParser.get(section, item)
            self._dict[section][item] = config
            # exception log
            logging.error(traceback.format_exc())


    def assemble(self):
        '''
        assemble config
        :return:
        '''
        if configParser.sections():
            for section in configParser.sections():
                options = configParser.options(section)
                if options:
                    for option in options:
                        self.parse(section, option)
