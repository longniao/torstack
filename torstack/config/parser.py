# -*- coding: utf-8 -*-

'''
torstack.config.container
config container definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

from tornado.options import define
from configparser import ConfigParser
import ast
from torstack.exception import BaseException
from torstack.config.default import *

configParser = ConfigParser()

class Parser(object):

    _dict = dict()

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
            self._dict[item] = config
        except:
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
