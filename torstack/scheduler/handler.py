# -*- coding: utf-8 -*-

'''
torstack.scheduler.handler
scheduler executor definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

from __future__ import absolute_import, unicode_literals

from tornado import gen
from tornado.web import url
from torstack.handler.scheduler import SchedulerHandler

class PauseJobHandler(SchedulerHandler):
    '''
    暂停某个任务
    '''
    @gen.coroutine
    def post(self):
        job_id = self.get_argument('job_id')
        self.pause_job(job_id)
        self.response_json("pause job:", job_id)

class ResumeJobHandler(SchedulerHandler):
    '''
    继续某个任务
    '''
    def post(self):
        jobId = self.get_argument('job_id')
        self.resume_job(job_id)
        self.response_json("resume job:", job_id)

class AddJobHandler(SchedulerHandler):
    '''
    添加任务
    '''

    @gen.coroutine
    def post(self):
        '''添加任务
            func － 执行的方法名
            args － 固定位置的方法参数
            kwargs － 可变的参数
            trigger － 触发规则 支持date ,interval,cron 三种
            trigger_args － 触发器参数
                date指定日期规则      参数实例： run_date＝datetime(2009, 11, 6, 16, 30, 5)
                interval间隔执行规则  参数：
                                    weeks (int) – number of weeks to wait
                                    days (int) – number of days to wait
                                    hours (int) – number of hours to wait
                                    minutes (int) – number of minutes to wait
                                    seconds (int) – number of seconds to wait
                                    start_date (datetime|str) – starting point for the interval calculation
                                    end_date (datetime|str) – latest possible date/time to trigger on
                                    timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations

                 实例：sched.add_job(job_function, 'interval', hours=2, start_date='2010-10-10 09:30:00', end_date='2014-06-15 11:00:00)

                cron执行规则   参考：http://apscheduler.readthedocs.io/en/latest/modules/triggers/cron.html#module-apscheduler.triggers.cron


            eg:('CustomerExecuter','interval', ['123'],{"content":"456"}, seconds=2)
        '''
        job_data = self.get_argument('job_data')
        json_data = self.get_json_data(job_data)

        func = json_data.get('job', '')
        trigger = json_data.get('trigger', '')
        args = json_data.get('args', [])
        kwargs = json_data.get('kwargs', {})
        trigger_args = json_data.get('trigger_args', {})
        result = self.add_job(func, trigger, args, kwargs, **trigger_args)
        print(result)
        self.response_json("add job success")


class RemoveJobHandler(SchedulerHandler):
    '''
    删除某个任务
    '''
    def post(self):
        job_id = self.get_argument('job_id')
        self.remove_job(job_id)
        self.response_json("remove job: %s" % job_id)

class RemoveAllJobsHandler(SchedulerHandler):
    '''
    删除所有任务
    '''
    def post(self):
        self.remove_all_jobs()
        self.response_json("remove all jobs")

class GetAllJobsHandler(SchedulerHandler):
    '''
    获取所有任务
    '''
    def get(self):
        result = self.get_jobs()
        self.response_json(result)


class StartHandler(SchedulerHandler):
    '''
    启动定时器
    '''
    def post(self):
        status = self.get_status()
        if status == True:
            self.response_json("Scheduler is already running")
        else:
            self.start_scheduler()
            result = self.get_status()
            self.response_json("start scheduler: %s" % result)

class ShutdownSchedHandler(SchedulerHandler):
    '''
    停止定时器
    '''
    def post(self):
        status = self.get_status()
        if status == True:
            self.shutdown_scheduler()
            self.response_json("shutdown scheduler")
        else:
            self.response_json("Scheduler is already shutdown")

class PauseSchedHandler(SchedulerHandler):
    '''
    暂停定时器
    '''
    def post(self):
        self.pause_scheduler()
        self.response_json("pause scheduler")

class ResumeSchedHandler(SchedulerHandler):
    '''
    重新启动定时器
    '''
    def post(self):
        self.resume_scheduler()
        self.response_json("resume scheduler")

class GetStatusHandler(SchedulerHandler):
    '''
    获取状态
    '''
    def get(self):
        status = self.get_status()
        self.response_json("scheduler status: %s" % status)

class SwitchSchedHandler(SchedulerHandler):
    '''
    开启/停止定时器
    '''
    def post(self):
        status = self.get_status()
        if status == True:
            self.shutdown_scheduler()
            self.response_json("shutdown scheduler")
        else:
            self.start_scheduler()
            self.response_json("start scheduler")


scheduler_handlers = [
    # job
    url(r"/scheduler/job_add", AddJobHandler, name='job_add'),
    url(r"/scheduler/job_pause", PauseJobHandler, name='job_pause'),
    url(r"/scheduler/job_resume", ResumeJobHandler, name='job_resume'),
    url(r"/scheduler/job_remove", RemoveJobHandler, name='job_remove'),
    url(r"/scheduler/job_remove_all", RemoveAllJobsHandler, name='job_remove_all'),
    url(r"/scheduler/job_list", GetAllJobsHandler, name='job_list'),
    # scheduler
    url(r"/scheduler/start", StartHandler, name='scheduler_start'),
    url(r"/scheduler/shutdown", ShutdownSchedHandler, name='scheduler_shutdown'),
    url(r"/scheduler/pause", PauseSchedHandler, name='scheduler_pause'),
    url(r"/scheduler/resume", ResumeSchedHandler, name='scheduler_resume'),
    url(r"/scheduler/status", GetStatusHandler, name='scheduler_status'),
    url(r"/scheduler/switch", SwitchSchedHandler, name='scheduler_switch'),
]