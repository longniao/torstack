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
            project_path=project_path,
            port=port,
            settings=settings,
            log=log,
        ),
        base=dict(
            session_enable=session_enable,
            session=session,
            cookie_enable=cookie_enable,
            cookie=cookie,
        ),
        rest=dict(
            rest_enable=rest_enable,
            rest=rest,
            rest_header=rest_header,
            rest_response=rest_response,
        ),
        websocket=dict(
            websocket_enable=websocket_enable,
            websocket=websocket,
        ),
        scheduler=dict(
            scheduler_enable=scheduler_enable,
            scheduler=scheduler,
            scheduler_executers=scheduler_executers,
        ),
        storage=dict(
            mysql_enable=mysql_enable,
            mysql_drive=mysql_drive,
            mysql=mysql,
            mongodb_enable=mongodb_enable,
            mongodb=mongodb,
            postgresql_enable=postgresql_enable,
            postgresql_drive=postgresql_drive,
            postgresql=postgresql,
            redis_enable=redis_enable,
            redis=redis,
            memcache_enable=memcache_enable,
            memcache=memcache,
        ),
        elasticsearch=dict(
            elasticsearch_enable=elasticsearch_enable,
            elasticsearch=elasticsearch,
        ),
        smtp=dict(
            smtp_enable=smtp_enable,
            smtp=smtp,
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
