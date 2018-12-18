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
        port=config_port,
        settings=config_settings,
        log=config_log,
        session=config_session,
        cookie=config_cookie,
        rest=config_rest,
        rest_header=config_rest_header,
        websocket=config_websocket,
        scheduler=config_scheduler,
        scheduler_executers=scheduler_executers,
        mysql=config_mysql,
        mongodb=config_mongodb,
        redis=config_redis,
        memcache=config_memcache,
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
            config = ast.literal_eval(configParser.get(section, item))
            if isinstance(config, dict):
                self._dict[item].update(config)
            else:
                self._dict[item] = config
        except Exception as e:
            logging.error(traceback.format_exc())

            varName = 'config_%s' % item
            if varName in locals() or varName in globals():
                self._dict[item] = varName

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
