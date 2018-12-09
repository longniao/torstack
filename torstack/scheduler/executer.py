# -*- coding: utf-8 -*-

'''
torstack.scheduler.executor
scheduler executor definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import logging

logger = logging.getLogger(__name__)


class SchedulerExecuter(object):

    def __init__(self):
        '''初始化
        '''
        self.id = ""
        self.path = ""

    @classmethod
    def run(self,*args,**kwargs):
        ''' 执行
        '''
        pass
