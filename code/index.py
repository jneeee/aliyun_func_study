# -*- coding: utf-8 -*-
import json

from utils.logger import log
from utils.db import DB
from task.checkin189 import runner as runner189

def initializer(context):
    global dbclient
    dbclient = DB()

def preStop(context):
    dbclient.close()
    log.info('db closed!')


def process189ret(ret):
    # 'checkin189' : {'time':x, 'checkin_space':x, 'lottery_space':x, 'total':x}
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
    log.info(f'run event: {event}')
    res = []
    event = json.loads(event)
    if isinstance(event.get('payload'), dict):
        for action in event.get('payload').get('actions'):
            if action == 'checkin189':
                ret = runner189(event)
                process189ret(ret)
                res.append(ret)
    log.info(f'Handler over, res: {res}')
    return res
