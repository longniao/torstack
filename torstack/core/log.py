# -*- coding: utf-8 -*-

'''
torstack.core.log
Basic log definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

from __future__ import (absolute_import, division, print_function, with_statement)

import os
import logging


class CoreLog(object):

    LOG_CONFIG = dict(
        filepath='/var/log',
    )

    def __init__(self, config={}):
        if config:
            self.LOG_CONFIG.update(config)

        folder = os.path.exists(self.LOG_CONFIG['filepath'])
        if not folder:
            os.makedirs(self.LOG_CONFIG['filepath'])

    def parse_msg(self, msg):
        '''
        parse msg
        :param msg:
        :return:
        '''
        if isinstance(msg, str):
            ret = '[STRING] [%s]' % msg
        elif isinstance(msg, dict):
            ret = '[DICT]'
            for key, value in msg.items():
                ret += ' [%s:%s]' % (key, str(value))
        elif isinstance(msg, list):
            ret = '[LIST]'
            for item in msg:
                ret += ' [%s]' % item
        elif isinstance(msg, tuple):
            ret = '[TUPLE]'
            for item in msg:
                ret += ' [%s]' % item
        else:
            ret = '[OTHER] [%s]' % msg

        return ret

    def genLogDict(self):
        '''
        default log config dict
        '''
        logDict = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "simple": {
                    'format': '%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s] - %(message)s'
                },
                'standard': {
                    'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s] - %(message)s'
                },
                'detail': {
                    'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s] [%(levelname)s] [%(pathname)s:%(lineno)d:%(funcName)s] - %(message)s'
                },
                'collect': {
                    'format': '%(asctime)s - %(message)s'
                }
            },

            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "formatter": "simple",
                },
                "access": {
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "level": "DEBUG",
                    "formatter": "standard",
                    "when": "midnight",
                    "filename": self.LOG_CONFIG['filepath'] + "/access_log.log",
                    # 'mode': 'a',
                    # "maxBytes": 1024*1024*10,  # 5 MB
                    "interval": 1,
                    "backupCount": 180,
                    "encoding": "utf-8"
                },
                "error": {
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "level": "WARNING",
                    "formatter": "detail",
                    "filename": self.LOG_CONFIG['filepath'] + "/error_log.log",
                    "when": "midnight",
                    "interval": 1,
                    "backupCount": 180,
                    "encoding": "utf-8",
                },
                "collect": {
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "level": "DEBUG",
                    "formatter": "collect",
                    "filename": self.LOG_CONFIG['filepath'] + "/collect_log.log",
                    "when": "midnight",
                    "interval": 1,
                    "backupCount": 180,
                    "encoding": "utf-8",
                },
            },
            "loggers": {
                "root": {
                    'handlers': ['console'],
                    'level': "INFO",
                    'propagate': False
                },
                "tornado.access": {
                    "level": "DEBUG",
                    "handlers": ["console", "access"],
                    "propagate": False
                },
                "error": {
                    "level": "DEBUG",
                    "handlers": ["console", "error"],
                    "propagate": False,
                },
                "collect": {
                    "level": "DEBUG",
                    "handlers": ["console", "collect"],
                    "propagate": False,
                },
            },
        }
        return logDict



if __name__ == "__main__":
    logDict = CoreLog().genLogDict()
    logging.config.dictConfig(logDict)

