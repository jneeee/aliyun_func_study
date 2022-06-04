# -*- coding: utf-8 -*-
from curses import curs_set
from flask import Flask, render_template
from flask import jsonify
from flask import request
import time
import functools
import json

from utils.logger import log
from utils.db import DB
from utils.tools import run_cmd


app = Flask(__name__)
app.debug = True

def clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        start_time = time.time()
        resp = func(*args, **kwargs)
        time_cost = time.time() - start_time
        log.info(f"{func.__name__} time_cost: {time_cost}")
        tempd = {
            'func_name': func.__name__,
            'resp': resp,
            'time_cost': time_cost,
        }
        return render_template('index.html', **tempd)
    return clocked

@app.route('/')
def route():
    return 'hello world'

@app.route('/runcmd')
def cmdhandler():
    log.info(f"request.headers.cmd: {request.headers.get('cmd')}")
    cmd = request.headers.get('cmd')
    if not cmd:
        return jsonify('err: cmd is "None"!')

    res = run_cmd(cmd)
    log.info(f'run cmd: {cmd}, {res}')
    return jsonify(res)

@app.route('/file')
def file():
    return 'comming'

@app.route('/db/<oprate>')
def get_key(oprate):
    #curl -H 'key: xxx'
    key = request.headers.get('key')
    log.info(f'req /db/{oprate}, key={key}')
    if oprate == 'select':
        if key == '*':
            key = None
        msg = dbclient.select(key)
        if not msg:
            msg = []
    elif oprate == 'delete':
        dbclient.delete(key)
        msg = 'Done'
    elif oprate == 'insert':
        value = request.headers.get('value')
        # true_oprate = insert or update
        if not value:
            return 'Need value'
        log.info(f'Insert value: {value}')
        try:
            value = json.loads(value)
        except json.decoder.JSONDecodeError as err:
            return str(err)
        # request.headers parse value into list
        # dbclient.select pickle.loads parse obj startswith [ get error 
        # msg = "Can't store value started with ["
        true_oprate = dbclient.insert(key, value)
        msg = f'msg: {true_oprate} {key}: {value}'
    elif oprate == 'append':
        cur_list = dbclient.select(key)
        if isinstance(cur_list, list):
            value = request.headers.get('value')
            cur_list.append(value)
            true_oprate = dbclient.insert(key, value)
            msg = f'{true_oprate} {key}: {cur_list}'
        else:
            msg = 'Error, cur value is not list type!'
    else:
        msg = {
            'error': f'Unknown oprate type: {oprate}',
            'oprate': 'select, delete, insert, append',
            'last_change_time': '2022-6-3 13:03:04',
        }
    log.info(msg)
    return jsonify(msg)

def initializer(context):
    global dbclient
    dbclient = DB()

def preStop(context):
    dbclient.close()

def handler(environ, start_response):
    return app(environ, start_response)

# print(f'__name__: {__name__}') __name__: app
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=2000)
