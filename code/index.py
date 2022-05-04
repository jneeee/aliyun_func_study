# -*- coding: utf-8 -*-
import json

from utils.logger import log
from utils.db import DB
import task

def initializer(context):
    global dbclient
    dbclient = DB()
    dbclient.insert('key1', 'value2')

def preStop(context):
    dbclient.close()
    log.info('db closed!')


def process189ret(ret):
    # 'checkin189' : {'time':x, 'checkin_space':x, 'lottery_space':x, 'total':x}
    before = dbclient.select('checkin189')
    if len(before) == 0:
        cur = dict()
        cur['checkin189'] = ret
        cur['checkin189']['tital'] = sum(v for k,v in ret if k != 'time')
    else:
        cur = json.loads(before[0].get('checkin189'))
        cur['total'] += sum(v for k,v in ret if k != 'time')
        cur.update(ret)
    dbclient.insert('checkin189', cur)
    log.info(f'store in db: cur: {cur}')

def handler(event):
    log.info(f'run event: {event}')
    res = []
    for action in event.get('actions'):
        ret = getattr(task, action).runner(event)
        if action == 'checkin189':
            process189ret(ret)
        res.append(ret)
    log.info(f'Handler over, res: {res}')
    return res
