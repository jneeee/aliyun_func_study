# -*- coding: utf-8 -*-
import json
import threading
import time

import task
from task.base import get_scheduler
from task.utils.logger import log, push_to_wx
from task.utils.db import kvdb

def initializer(context):
    pass


def preStop(context):
    push_to_wx(log.msg_box)
    kvdb.close()
    log.debug('db closed!')


def dailyhandler(event):
    func_d = {
        # 'acfun': acfun,
    }
    # dailytask: {date: 20220529, task_d: {checkin189: 0 ...}}
    dailytask = kvdb.select('dailytask')
    cur_time = time.strftime("%Y%m%d")
    if not dailytask or cur_time != dailytask.get('date'):
        dailytask = {
            'date': cur_time,
            'task_d': dict.fromkeys(func_d.keys(), 0),
        }
    for task, run_count in dailytask['task_d'].items():
        if not run_count:
            if task == 'Bilibili':
                # Due to asycnio, Bilibili run in main thread.
                continue
                func_d.get(task).runner()
            else:
                threading.Thread(target=func_d.get(task).runner).start()
            dailytask['task_d'][task] += 1
        else:
            log.info(f'{task} already runned today')
    kvdb.insert('dailytask', dailytask)


def _dailyhandler(payload, sched):
    for job in getattr(task, payload):
        job_ins = job()
        sched.add_job(job_ins.run, id=job_ins.name)
    sched.start()
    print('sched start')
    sched.shutdown()


def _run_task_list(payload, sched):
    for job_name in payload:
        sched.add_job(getattr(task, job_name).run, id=job_name)
    sched.start()
    sched.shutdown()


def handler(event, context):
    # type(event): <class 'bytes'>
    event = json.loads(event)
    log.info(f'Handler event: {event}')
    payload = event.get('payload')
    sched = get_scheduler()
    if 'dailytask' == payload:
        _dailyhandler(payload, sched)
    elif isinstance(payload, list):
        # run a task list
        _run_task_list(payload, sched)
