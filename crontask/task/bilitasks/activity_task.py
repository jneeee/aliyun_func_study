import time
import asyncio, json
import collections

from BiliClient import asyncbili
from task.utils.db import DB
from task.utils.logger import log as logging


activity_task_lock = asyncio.Lock()
activity_task_path = {}

def get_act_json(task_config):
    activity_list = []
    if 'path' in task_config:
        if task_config["path"] in activity_task_path:
            activity_list.extend(activity_task_path[task_config["path"]])
        else:
            try:
                with open(task_config["path"], 'r', encoding='utf-8') as fp:
                    activity_task_path[task_config["path"]] = json.load(fp)
            except Exception as e:
                logging.warning(f'读取活动列表异常：{str(e)})')
            else:
                activity_list.extend(activity_task_path[task_config["path"]])
    if 'activities' in task_config:
        activity_list.extend(task_config["activities"])
    return activity_list

async def activity_task(biliapi: asyncbili,
                        task_config: dict
                        ) -> None:
    activity_list = get_act_json(task_config)
    log_d = collections.defaultdict(list)
    for x in activity_list:
        try:
            op_code = 3
            ret = await biliapi.activityAddTimes(x["sid"], op_code)
            add_num = ret['data']['add_num']
            if add_num > 0:
                pass
                # logging.info(f'{biliapi.name}: 【抽奖】{x["name"]}增加次数: {add_num}')
        except Exception as e:
            logging.warning(f'{biliapi.name}: 增加({x["name"]})活动抽奖次数异常：({str(e)})')

        try:
            ret = await biliapi.activityMyTimes(x["sid"])
            if ret["code"] == 0:
                times = ret["data"]["times"]
            else:
                logging.info(f'{biliapi.name}: 获取({x["name"]})活动抽奖次数错误，消息为({ret["message"]})')
                continue
        except Exception as e:
            logging.warning(f'{biliapi.name}: 获取({x["name"]})活动抽奖次数异常，原因为({str(e)})，跳过参与活动')
            continue

        for ii in range(times):
            try:
                async with activity_task_lock:
                    ret = await biliapi.activityDo(x["sid"], 1)
                    if ret["code"]:
                        if '请求过于频繁' in ret["message"]:
                            logging.error('抽奖请求过于频繁，请稍后再试')
                    else:
                        log_d[x["name"]].append(ret["data"][0]["gift_name"])
                        # logging.info(f'{biliapi.name}: 参与({x["name"]})活动第({ii + 1}/{times})次，结果为({ret["data"][0]["gift_name"]})')
            except Exception as e:
                logging.warning(f'{biliapi.name}: 参与({x["name"]})活动异常，原因为({str(e)})')
            finally:
                await asyncio.sleep(1)
    logging.info(log_d)

def activity_runner():
    # not use
    dbclient = DB()
    today = time.strftime("bili_act_%Y%m%d")

    act_list = dbclient.select(today)
    if not act_list:
        act_list = get_act_json()
        cur_act = act_list.pop()
        dbclient.insert(today, act_list)
    else:
        cur_act = act_list.pop()
        dbclient.insert(today, act_list)
    # run_single_act_task(cur_act)

