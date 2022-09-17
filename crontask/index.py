# -*- coding: utf-8 -*-
import json
import threading
import time

from utils.logger import log, push_to_wx
from utils.db import kvdb
from task import checkin189
from task import BiliExp
from task import smzdm
from task.acfun import acfun

def initializer(context):
    pass

def preStop(context):
    push_to_wx(log.msg_box)
    kvdb.close()
    log.debug('db closed!')

def dailyhandler(event):
    func_d = {
        'Cloud189': checkin189,
        'Bilibili': BiliExp,
        'Smzdm': smzdm,
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

def handler(event, context):
    # type(event): <class 'bytes'>
    event = json.loads(event)
    log.info(f'Handler event: {event}')
    if 'dailytask' in event.get('payload'):
        dailyhandler(event)
