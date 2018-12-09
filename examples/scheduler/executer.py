# -*- coding: utf-8 -*-

'''
torstack.example.scheduler.executer
scheduler executer definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

from torstack.scheduler.executer import SchedulerExecuter
import time

class TestExecuter(SchedulerExecuter):
    '''
    Test Executer
    '''

    id = "TestExecuter"
    path = "scheduler.executer:TestExecuter.run"

    def __init__(self):
        '''
        init
        '''
        super(TestExecuter, self).__init__()

    @classmethod
    def run(cls, *args, **kwargs):
        ''' 执行
        '''
        print('TestExecuter run @ %s' % time.time())