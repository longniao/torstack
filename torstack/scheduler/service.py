# -*- coding: utf-8 -*-

'''
torstack.scheduler.service
service definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import logging

from torstack.scheduler.model import SchedulerJob

logger = logging.getLogger(__name__)


class SchedulerService(object):

    @staticmethod
    def list_data(db_session):
        with db_session.session_ctx() as session:
            session.commit()
            dataList = session.query(SchedulerJob).all()
            return dataList

    @staticmethod
    def delete_data(db_session, id):
        with db_session.session_ctx(bind='master') as session:
            count = session.query(SchedulerJob).filter(SchedulerJob.id == id).delete()
            if count:
                session.commit()
            return count

    @staticmethod
    def update_data(db_session, id, data_to_update):
        with db_session.session_ctx(bind='master') as session:
            if "id" in data_to_update:
                data_to_update.remove("id")

            data_to_update = SchedulerJob(**data_to_update)
            count = session.query(SchedulerJob).filter(SchedulerJob.id == id).update(data_to_update)
            if count:
                session.commit()
            return count
