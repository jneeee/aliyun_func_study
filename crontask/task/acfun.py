# -*- coding: utf-8 -*-
import requests

from task.config import acfun_config
from task.utils.logger import log
from task.base import Jobadapter

class AcFunCheckIn(Jobadapter):
    def __init__(self):
        self.contentid = None

    def set_session(self):
        self.session = requests.session()
        headers = {
            "acPlatform": "IPHONE",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62",
            "devicetype": "0",
            "accept-language": "zh-Hans-CN;q=1, en-CN;q=0.9, ja-CN;q=0.8, zh-Hant-HK;q=0.7, io-Latn-CN;q=0.6",
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded",
        }
        self.session.headers = headers
        cookies = {
            "acPasstoken": acfun_config.acPasstoken,
            "auth_key": acfun_config.auth_key,
            "kpn": "ACFUN_APP",
        }
        self.session.cookies.update(cookies)
        self._update_api_st()

    def _update_api_st(self):
        url = "https://id.app.acfun.cn/rest/web/token/get"
        resp = self.session.post(url=url, data="sid=acfun.midground.api").json()
        # resp {'result': 0, 'ssecurity': '' 'userId': , 'acfun.midground.api_st': '', 'acfun.midground.api.at': ''}
        self.session.cookies['acfun.midground.api_st'] = resp['acfun.midground.api_st']
        log.info('_update_api_st() success')

    def get_video(self):
        url = "https://www.acfun.cn/rest/pc-direct/rank/channel"
        data = {'channelId': 0, 'rankPeriod': 'DAY'}
        self.video_info = self.session.get(url=url, params=data).json().get("rankList")[5]

    def sign_daily(self):
        # 签到
        url = "https://www.acfun.cn/rest/pc-direct/user/signIn"
        resp = self.session.post(url=url).json()
        # resp = {'result': 0, 'msg': '签到已成功，领取3蕉', 'bananaDelta': 3, 'host-name': 'hb2-acfun-kce-node85.aliyun'}
        log.info(resp['msg'])

    @staticmethod
    def add_danmu(self):
        # TODO videoId: 这个字段像是弹幕库ID?没搞清楚，所以没法做到动态发弹幕
        url = "https://www.acfun.cn/rest/pc-direct/new-danmaku/add"
        body = {
            'body': 'acfun', 'mode': 1, 'size': 25, 'roleId': '',
            'id': 10520443, 'videoId': 10489058,
            'color': 16777215, 'position': 13163, 'type': 'douga',
            'subChannelId': 60, 'subChannelName': '娱乐',
        }
        resp = self.session.post(url=url, data=body).json()
        if resp.get("result") == 0:
            msg = "弹幕成功"
        else:
            msg = "弹幕失败"
        log.info(msg)

    def throwbanana(self):
        url = "https://www.acfun.cn/rest/pc-direct/banana/throwBanana"
        body = f"count=1&resourceId={self.contentid}&resourceType=2"
        body1 = {'count': 1, 'resourceId': 37461710, 'resourceType':2}
        response = self.session.post(url=url, data=body)
        if response.json().get("result") == 0:
            msg = "投蕉成功"
        else:
            msg = "投蕉失败"
        log.info(msg)

    def _like_video(self):
        like_url = "https://kuaishouzt.com/rest/zt/interact/add"
        unlike_url = "https://kuaishouzt.com/rest/zt/interact/delete"
        data = f"interactType=1&objectId={self.contentid}&objectType=2&subBiz=mainApp"
        response = self.session.post(url=like_url, data=data)
        # self.session.post(url=unlike_url, data=data)
        if response.json().get("result") == 1:
            log.info("点赞成功")
        else:
            log.error("点赞失败")

    def share_task(self):
        url = "https://api-ipv6.acfunchina.com/rest/app/task/reportTaskAction"
        params = {
            "market": "tencent",
            "taskType": "1",
            "product": "ACFUN_APP",
            "appMode": "0",
        }
        import pdb;pdb.set_trace()
        resp = self.session.get(url=url, params=params).json()
        if resp.get('result') == 0:
            log.info('分享成功')
        else:
            log.error('分享失败')

    def run(self):
        self.set_session()
        self.get_video()
        self.sign_daily()
        # self.add_danmu() wrong video ID
        self._like_video()
        # 以下任务报错
        # self.throwbanana()
        # self.share_task()
