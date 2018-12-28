# -*- coding: utf-8 -*-

'''
torstack.handler.scheduler
job scheduler definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import logging
import pickle
from torstack.handler.webrest import WebRestHandler
from torstack.scheduler.service import SchedulerService

logger = logging.getLogger(__name__)

class SchedulerHandler(WebRestHandler):

    def initialize(self):
        '''
        Init
        '''
        super(SchedulerHandler, self).initialize()
        self.taskmgr = self.application.taskmgr
        self.dbname = 'test'
        self.db = self.storage['sync_mysql']

    def get_status(self):
        '''
        获取运行状态
        :return:
        '''
        return self.taskmgr.scheduler.running

    def add_job(self,func,trigger,args,kwargs,**trigger_args):
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
        #return self.taskmgr.scheduler.add_job('sys:stdout.write', 'interval', seconds=3, args=args,kwargs=kwargs)

        funcPath = self.taskmgr.executers.get(func)

        if not funcPath:
            raise ValueError('Executer not found for name [%s]' % func)

        if not trigger in ("date","interval","cron"):
            raise ValueError('trigger not allow for name [%s]' % trigger)

        return self.taskmgr.scheduler.add_job(funcPath, trigger,args=args,kwargs=kwargs, **trigger_args)

    def modify_job(self, job_id, **changes):
        return self.taskmgr.scheduler.modify_job(job_id, None, **changes)

    def reschedule_job(self, job_id, trigger=None, **trigger_args):
        result = self.taskmgr.scheduler.reschedule_job(job_id, None, trigger, **trigger_args)
        return job_id

    def pause_job(self, job_id):
        '''
        暂停
        :param job_id:
        :return:
        '''
        return self.taskmgr.scheduler.pause_job(job_id)

    def resume_job(self, job_id):
        '''

        :param job_id:
        :return:
        '''
        return self.taskmgr.scheduler.resume_job(job_id)

    def remove_job(self, job_id):
        '''
        移除
        :param job_id:
        :return:
        '''
        return self.taskmgr.scheduler.remove_job(job_id)

    def remove_all_jobs(self):
        '''
        移除全部
        :return:
        '''
        return self.taskmgr.scheduler.remove_all_jobs()

    def get_job(self, job_id):
        '''
        查看任务
        :param job_id:
        :return:
        '''
        return self.taskmgr.scheduler.get_job(job_id)

    def get_jobs(self):
        '''
        查询任务列表
        :return:
        '''
        if self.taskmgr.storage=="sync_mysql":
            datas = SchedulerService.list_data(self.db)
            return self.modeltoJson(datas)
        elif self.taskmgr.storage=="mongodb":
            results = []
            dbname = self.taskmgr.dbname
            for doc in self.taskmgr.driver[dbname]['scheduler_tasks'].find():
                doc["id"] = doc.get("_id")
                results.append(doc)
            return results

    def modeltoJson(self,obj):
        ''' mysql model转dict
        '''
        if not obj:
            return []
        if isinstance(obj,list):
            result = []
            for o in obj:
                result.append(self.modeltoJson(o))
            return result
        else:
            return self._jobToJson(pickle.loads(obj.job_state))
            return {
                'id': obj.id,
                'next_run_time': obj.next_run_time,
                'job_state': pickle.loads(obj.job_state),
            }
            # return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

    def _jobToJson(self,job):
        '''job对象转为json
        '''

        if not job:return None

        return {
            "id"                 : job['id'],
            "name"               : job['name'],
            "trigger"            : str(job['trigger']),
            "func"               : job['func'],
            "args"               : job['args'],
            "kwargs"             : job['kwargs'],
            "executor"           : job['executor'],
            "max_instances"      : job['max_instances'],
            "next_run_time"      : str(job['next_run_time']),
            "misfire_grace_time" : job['misfire_grace_time'],
            "coalesce"           : job['coalesce'],
            "version"            : job['version'],
        }




    def start_scheduler(self):
        '''
        启动
        :return:
        '''
        self.taskmgr.scheduler.start()
        return self.taskmgr.scheduler.running

    def shutdown_scheduler(self):
        '''
        停止
        :return:
        '''
        try:
            return self.taskmgr.scheduler.shutdown()
        except Exception as e:
            print('Unable to shutdown scheduler. %s' % e)

    def pause_scheduler(self):
        '''
        暂停
        :return:
        '''
        return self.taskmgr.scheduler.pause()

    def resume_scheduler(self):
        '''
        重新启动
        :return:
        '''
        return self.taskmgr.scheduler.resume()
