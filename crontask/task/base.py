# -*- coding: utf-8 -*-
import abc
from pytz import utc

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

# from utils.logger import log
# from utils.db import dbclient


class Task:
    task_queue = []
    # TODO(jn) 关系数据库持久化存储
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def run(self):
        # Overwrite me
        raise NotImplementedError

    @property
    def is_runned_today(self):
        pass

    @property
    def name(self):
        return self.__class__.__name__
 
 
def get_scheduler():
    # return: A tasks flow that can be run
    jobstores = {
        'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite'),
    }
    executors = {
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(5),
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 3,
    }
    scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, 
        job_defaults=job_defaults, timezone=utc)
    return scheduler
