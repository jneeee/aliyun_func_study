import base64
import os
import re
import time

import requests
import rsa

from task.utils.logger import log
from task.utils.db import kvdb
from task.base import Jobadapter


class CheckIn:
    client = requests.Session()
    login_url = "https://cloud.189.cn/api/portal/loginUrl.action?" \
                "redirectURL=https://cloud.189.cn/web/redirect.html?returnURL=/main.action"
    submit_login_url = "https://open.e.189.cn/api/logbox/oauth2/loginSubmit.do"
    sign_url = ("https://api.cloud.189.cn/mkt/userSign.action?rand=%s"
                "&clientType=TELEANDROID&version=8.6.3&model=SM-G930K")

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.res = {}

    def check_in(self):
        self.res['time'] = time.strftime("%Y-%m-%d %H:%M:%S")
        self.login()
        rand = str(round(time.time() * 1000))
        url = "https://m.cloud.189.cn/v2/drawPrizeMarketDetails.action?taskId=TASK_SIGNIN&activityId=ACT_SIGNIN"
        url2 = "https://m.cloud.189.cn/v2/drawPrizeMarketDetails.action?taskId=TASK_SIGNIN_PHOTOS&activityId=ACT_SIGNIN"
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; SM-G930K Build/NRD90M; wv)"
                          " AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74"
                          ".0.3729.136 Mobile Safari/537.36 Ecloud/8.6.3 Android/22 clie"
                          "ntId/355325117317828 clientModel/SM-G930K imsi/46007111431782"
                          "4 clientChannelId/qq proVersion/1.0.6",
            "Referer": "https://m.cloud.189.cn/zhuanti/2016/sign/index.jsp?albumBackupOpened=1",
            "Host": "m.cloud.189.cn",
            "Accept-Encoding": "gzip, deflate",
        }
        response = self.client.get(self.sign_url % rand, headers=headers)
        net_disk_bonus = response.json()["netdiskBonus"]
        if response.json()["isSign"] == "false":
            log.info(f"未签到，签到获得 {net_disk_bonus}M 空间")
        else:
            log.info(f"已经签到过了，签到获得 {net_disk_bonus}M 空间")
        self.res['checkin_space'] = int(net_disk_bonus)

        self.res['lottery_space'] = 0
        response = self.client.get(url, headers=headers)
        if "errorCode" in response.text:
            log.info(response.text)
        else:
            prize_name = (response.json() or {}).get("prizeName")
            log.info(f"抽奖获得 {prize_name}")
            self.res['lottery_space'] += 50
        response = self.client.get(url2, headers=headers)
        if "errorCode" in response.text:
            log.info(response.text)
        else:
            prize_name = (response.json() or {}).get("prizeName")
            log.info(f"抽奖获得 {prize_name}")
            self.res['lottery_space'] += 50
        return self.res

    @staticmethod
    def rsa_encode(rsa_key, string):
        rsa_key = f"-----BEGIN PUBLIC KEY-----\n{rsa_key}\n-----END PUBLIC KEY-----"
        pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(rsa_key.encode())
        result = b64_to_hex((base64.b64encode(rsa.encrypt(f"{string}".encode(), pubkey))).decode())
        return result

    def login(self):
        r = self.client.get(self.login_url)
        captcha_token = re.findall(r"captchaToken' value='(.+?)'", r.text)[0]
        lt = re.findall(r'lt = "(.+?)"', r.text)[0]
        return_url = re.findall(r"returnUrl = '(.+?)'", r.text)[0]
        param_id = re.findall(r'paramId = "(.+?)"', r.text)[0]
        j_rsa_key = re.findall(r'j_rsaKey" value="(\S+)"', r.text, re.M)[0]
        self.client.headers.update({"lt": lt})
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/76.0",
            "Referer": "https://open.e.189.cn/",
        }
        data = {
            "appKey": "cloud",
            "accountType": "01",
            "userName": f"{{RSA}}{self.rsa_encode(j_rsa_key, self.username)}",
            "password": f"{{RSA}}{self.rsa_encode(j_rsa_key, self.password)}",
            "validateCode": "",
            "captchaToken": captcha_token,
            "returnUrl": return_url,
            "mailSuffix": "@189.cn",
            "paramId": param_id,
        }
        resp = self.client.post(self.submit_login_url,
                             data=data, headers=headers, timeout=5).json()
        log.info(f'checkin189: {resp["msg"]}')
        if '图形验证码错误' in resp["msg"]:
            raise Exception("账户风控中，请手动登录后重试")
        redirect_url = resp.get("toUrl")
        if redirect_url:
            self.client.get(redirect_url)


def b64_to_hex(a):
    def _chr(c):
        return "0123456789abcdefghijklmnopqrstuvwxyz"[c]
    B64MAP = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    d = ""
    e = 0
    c = 0
    for i in range(len(a)):
        if list(a)[i] != "=":
            v = B64MAP.index(list(a)[i])
            if 0 == e:
                e = 1
                d += _chr(v >> 2)
                c = 3 & v
            elif 1 == e:
                e = 2
                d += _chr(c << 2 | v >> 4)
                c = 15 & v
            elif 2 == e:
                e = 3
                d += _chr(c)
                d += _chr(v >> 2)
                c = 3 & v
            else:
                e = 0
                d += _chr(c << 2 | v >> 4)
                d += _chr(15 & v)
    if e == 1:
        d += _chr(c << 2)
    return d


class checkin189cloud(Jobadapter):
    def __init__(self) -> None:
        super().__init__()

    def run(self):
        login_info = [os.environ.get('phone'), os.environ.get('pswd189')]
        if not all(login_info):
            log.error('phone or passwd is None, skip task!')
            return
        res = CheckIn(*login_info).check_in()
        self._process189ret(res)
        return res

    def _process189ret(self, ret):
        # 'checkin189' : {'time':x, 'checkin_space':x, 'lottery_space':x, 'total':x}
        if not ret:
            log.error(f'process189ret get empty ret')
            return
        before = kvdb.select('checkin189')
        if not before:
            ret['total'] = sum([v for k,v in ret.items() if k != 'time'])
            cur = ret
        else:
            cur = before
            cur['total'] += sum([v for k,v in ret.items() if k != 'time'])
            cur.update(ret)

        kvdb.insert('checkin189', cur)
        log.info(f'store in db: "checkin189": {cur}')
