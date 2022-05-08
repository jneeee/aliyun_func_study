# -*- coding: utf-8 -*-
import json

from utils.logger import log
from utils.db import DB
from task.checkin189 import runner as runner189
from task.BiliExp import runner as runner_b


def initializer(context):
    log.debug('db connect!')
    global dbclient
    dbclient = DB()

def preStop(context):
    dbclient.close()
    log.info('db closed!')

def need_run_check189():
    pass

def process189ret(ret):
    # 'checkin189' : {'time':x, 'checkin_space':x, 'lottery_space':x, 'total':x}
    if not ret:
        log.error(f'process189ret get empty ret')
        return
    before = dbclient.select('checkin189')
    if not before:
        ret['total'] = sum([v for k,v in ret.items() if k != 'time'])
        cur = ret
    else:
        cur = before.get('checkin189')
        cur['total'] += sum([v for k,v in ret.items() if k != 'time'])
        cur.update(ret)
    dbclient.insert('checkin189', cur)
    log.info(f'store in db: "checkin189": {cur}')

def handler(event, context):
    res = {}
    log.info(f'type(event): {type(event)}')

    event = json.loads(event)
    log.info(f'Handler event: {event}')
    for action in json.loads(event.get('payload')).get('actions', []):
        if action == 'checkin189':
            ret = runner189(event)
            process189ret(ret)
        if action == 'b_checkin':
            ret = runner_b()
        res[action] = ret
    log.info(f'Handler over, res: {res}')
    return res
