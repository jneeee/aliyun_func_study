# -*- coding: utf-8 -*-
from flask import Flask, make_response, render_template
from flask import jsonify
from flask import request
import subprocess
import time
import functools

from aliyun.log import *

from utils.logger import log
from utils.db import DB


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
def runcmd():
    log.info(f'request.args: {request.args}')
    cmd = request.args.get('cmd')
    if not cmd:
        return jsonify('err: cmd is "None"!')
    out, err = map(str, subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate())
    response_body = {'cmd': cmd,'out': out, 'err': err}
    log.info(f'run cmd: {cmd}, {response_body}')
    return jsonify(response_body)

@app.route('/file')
def file():
    return 'comming'

@app.route('/db/<key>')
@clock
def get_key(key):
    log.info(f'req /db/{key}')
    data = dbclient.select(key)
    if not data:
        data = {key: 'None'}
    return data

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
