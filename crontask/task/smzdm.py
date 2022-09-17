# coding=utf-8
import requests
from task.utils.logger import log


class SMZDM_Bot(object):
    def __init__(self):
        self.session = requests.Session()
        DEFAULT_HEADERS = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'zhiyou.smzdm.com',
            'Referer': 'https://www.smzdm.com/',
            'Sec-Fetch-Dest': 'script',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        }
        self.session.headers = DEFAULT_HEADERS

    def checkin(self):
        url = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'
        msg = self.session.get(url)
        try:
            return msg.json()
        except Exception as e:
            return msg.content

def main():
    sb = SMZDM_Bot()
    cookies = (
        'sess=AT-yD961u6lkViu/dbhpqU87mjwsatFsbatFRnLzPctFMzr8OU9JM3n7M2XtijKnuGY7EoPq/XjdNpQsz1mW7mQGdJ4a/PWRGM+u2snzBf28LROyegBHt0nvS4=;'
        'smzdm_id=6764311198;'
        'user=user:6764311198|6764311198;'
    )
    sb.session.headers['Cookie'] = cookies
    data = sb.checkin()
    if not data.get('error_code'):
        info = f"smzdm: 已经签到: {data['data']['continue_checkin_days']}天"
        log.info(info)
    else:
        log.warning(f"smzdm: {data}")

def runner():
    main()
