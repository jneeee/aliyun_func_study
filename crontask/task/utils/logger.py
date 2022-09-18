import logging
import requests

class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

class MyLogHandler(logging.Handler, Singleton):
    def __init__(self):
        super().__init__()

    def emit(self, record, push=True):
        try:
            if push:
                msg_str = self.format(record)
                log.msg_box.append(msg_str)
        except Exception:
            self.handleError(record)

def push_to_wx(content):
    url = "https://sctapi.ftqq.com/xxxxxx.send"
    data = {
        'title': '阿里云函数 crontask',
        'desp': str(content),
        # desp must be str
    }
    # log.error(f'push_to_wx content: {content}')
    requests.post(url, data=data)

log = logging.getLogger()
log.addHandler(MyLogHandler())
if not hasattr(log, 'msg_box'):
    log.msg_box = []
