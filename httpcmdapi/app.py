# -*- coding: utf-8 -*-
from flask import Flask
from flask import jsonify
from flask import request

import logging
import subprocess

app = Flask(__name__)
app.debug = True
logger = logging.getLogger()


@app.route('/')
def route():
    return 'hello world'

@app.route('/runcmd')
def runcmd():
    logger.info(f'request.args: {request.args}')
    cmd = request.args.get('cmd')
    if not cmd:
        return jsonify('err: cmd is "None"!')
    out, err = map(str, subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate())
    response_body = {'cmd': cmd,'out': out, 'err': err}
    logger.info(f'run cmd: {cmd}, {response_body}')
    return jsonify(response_body)

@app.route('/file')
def file():
    return 'comming'

def initializer(context):
    print('initializer')

def preStop(context):
    print('preStop')

def handler(environ, start_response):
    return app(environ, start_response)

# print(f'__name__: {__name__}') __name__: app
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=2000)
