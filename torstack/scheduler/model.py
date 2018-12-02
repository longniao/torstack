# -*- coding: utf-8 -*-

'''
torstack.scheduler.model
scheduler model definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

from sqlalchemy import CHAR, Column, DECIMAL, Float, INTEGER, Index, LargeBinary, String, TIMESTAMP, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SchedulerJob(Base):
    __tablename__ = 'scheduler_job'

    id = Column(String(191), primary_key=True)
    next_run_time = Column(Float(asdecimal=True), index=True)
    job_state = Column(LargeBinary, nullable=False)


class SchedulerLog(Base):
    __tablename__ = 'scheduler_log'

    id = Column(INTEGER, primary_key=True)
    task_id = Column(String(45))
    job_id = Column(String(45))
    content = Column(String(500))
    created_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))


class SchedulerTask(Base):
    __tablename__ = 'scheduler_task'

    id = Column(String(40), primary_key=True)
    name = Column(String(100))
    created_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    create_person = Column(String(10))