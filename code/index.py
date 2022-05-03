# -*- coding: utf-8 -*-
import logging

from utils.db import DB

def initializer(context):
    global dbclient, logger
    dbclient = DB()
    dbclient.insert('key1', 'value2')
    logger = logging.getLogger()

def preStop(context):
    dbclient.close()
    print('db closed!')

def handler(event, context):
    r = dbclient.select('key1')
    logger.info(f'event: {event}')
    logger.info(f'initializing test, db key1: {r}')

    return r
