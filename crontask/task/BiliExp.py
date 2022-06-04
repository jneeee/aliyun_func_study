# -*- coding: utf-8 -*-
from json import loads
import asyncio, time, sys, os
import random, argparse, datetime
from importlib import import_module
from collections import OrderedDict

from . import BiliClient
from . import bilitasks
from utils.logger import log as logging

# /code/task
sys.path.append(f'{os.getcwd()}/task')
main_version = (1, 2, 1)
main_version_str = '.'.join(map(str, main_version))

def convertTimeString(time_string: str):
    '''
    转换字符串为时间对象
    time_string str 时间字符串
    '''
    return datetime.datetime.strptime(time_string,'%H:%M:%S').time()

def load_config(path: str) -> OrderedDict:
    '''加载配置文件'''
    if path:
        with open(path,'r',encoding='utf-8') as fp:
            return loads(fp.read(), object_pairs_hook=OrderedDict)
    else:
        for path in ('./task/config/config.json', './config.json'):
            if os.path.exists(path):
                with open(path,'r',encoding='utf-8') as fp:
                    return loads(fp.read(), object_pairs_hook=OrderedDict)
        raise RuntimeError('未找到配置文件')

async def start(configData: dict):
    '''开始任务'''
    config_version = configData.get('version', '1.0.0')
    if tuple(map(int, config_version.strip().split('.'))) == main_version:
        logging.debug(f'当前程序版本为v{main_version_str},配置文件版本为v{config_version}')
    else:
        logging.warning(f'当前程序版本为v{main_version_str},配置文件版本为v{config_version},版本不匹配可能带来额外问题')
        bilitasks.webhook.addMsg('msg_simple', '配置文件版本不匹配\n')

    await asyncio.wait([asyncio.ensure_future(run_user_tasks(user, configData["default"], configData.get("http_header", None))) for user in configData["users"]]) #执行任务
    await bilitasks.webhook.send() #推送消息

async def run_user_tasks(user: dict,           #用户配置
                         default: dict,        #默认配置
                         header: dict = None
                         ) -> None:
    async with BiliClient.asyncbili(header) as biliapi:
        try:
            if not await biliapi.login_by_cookie(user["cookieDatas"]):
                logging.warning(f'id为{user["cookieDatas"]["DedeUserID"]}的账户cookie失效，跳过此账户后续操作')
                bilitasks.webhook.addMsg('msg_simple', f'id为{user["cookieDatas"]["DedeUserID"]}的账户cookie失效\n')
                return
        except Exception as e:
            logging.warning(f'登录验证id为{user["cookieDatas"]["DedeUserID"]}的账户失败，原因为{str(e)}，跳过此账户后续操作')
            return

        show_name = user.get("show_name", "")
        if show_name:
            biliapi.name = show_name

        logging.info(f'{biliapi.name}: 等级 {biliapi.level},经验 {biliapi.myexp},剩余硬币 {biliapi.mycoin}')
        bilitasks.webhook.addMsg('msg_simple', f'{biliapi.name}: 等级{biliapi.level},经验{biliapi.myexp},剩余硬币{biliapi.mycoin}\n')

        task_array = [] #存放本账户所有任务
        for task in default: #遍历任务列表，把需要运行的任务添加到task_array

            try:
                task_module = import_module(f'task.bilitasks.{task}') #加载任务模块
            except ModuleNotFoundError:
                logging.error(f'{biliapi.name}: 未找到任务模块{task}')
                continue

            task_function = getattr(task_module, task, None)
            if not task_function:
                logging.error(f'{biliapi.name}: 未找到任务{task}的入口函数')
                continue

            if task in user["tasks"]:
                if isinstance(user["tasks"][task], bool):
                    if user["tasks"][task]:
                        task_array.append(asyncio.ensure_future(task_function(biliapi)))
                elif isinstance(user["tasks"][task], dict):
                    if 'enable' in user["tasks"][task] and user["tasks"][task]["enable"]:
                        task_array.append(asyncio.ensure_future(task_function(biliapi, user["tasks"][task])))

            else:
                if isinstance(default[task], bool):
                    if default[task]:
                        task_array.append(asyncio.ensure_future(task_function(biliapi)))
                elif isinstance(default[task], dict):
                    if 'enable' in default[task] and default[task]["enable"]:
                        task_array.append(asyncio.ensure_future(task_function(biliapi, default[task])))

        if task_array:
            await asyncio.wait(task_array)        #异步等待所有任务完成

def _debug(task_name, configData):
    if not task_name:
        return
    elif task_name not in configData['default']:
        logging.error(f'没有此任务：{task_name}')
    else:
        configData['default'] = {task_name:configData['default'][task_name]}

def main(args):
    try:
        configData = load_config(args.get("configfile",None))
    except Exception as e:
        print(f'配置加载异常，原因为{str(e)}，退出程序')
        sys.exit(6)

    if args.get("logfile", None):
        configData["log_file"] = args.get("logfile")

    if "looping" not in configData:
        configData["looping"] = None
    if "random" not in configData:
        configData["random"] = None
    if "timing" not in configData:
        configData["timing"] = []

    for i in range(len(configData["timing"])):
        configData["timing"][i]=convertTimeString(configData["timing"][i])
    _debug(args.get('debug'), configData)

    looping = args.get("looping",None) or configData["looping"]
    timing = args.get("timing",[]) or configData["timing"]
    random_max = args.get("random",None) or configData["random"]
    #启动任务
    # loop = asyncio.get_running_loop()
    loop = asyncio.new_event_loop()
    if looping:
        while True:
            task=loop.create_task(start(configData))
            loop.run_until_complete(task)
            time.sleep(looping)
            if random_max:
                random_time = random.randint(1, random_max)
                logging.info(f'随机延时{random_time}s')
                time.sleep(random_time)
    elif timing:
        while True:
            now = datetime.datetime.now().time().replace(microsecond=0)
            if now in timing: # 此处为设置的每天定时的时间
                if random_max:
                    random_time = random.randint(1, random_max)
                    logging.info(f'随机延时{random_time}s')
                    time.sleep(random_time)
                task=loop.create_task(start(configData))
                loop.run_until_complete(task)
                time.sleep(2)
    else:
        if random_max:
            random_time = random.randint(1, random_max)
            logging.info(f'随机延时{random_time}s')
            time.sleep(random_time)
        task = loop.create_task(start(configData))
        loop.run_until_complete(task)

def runner():
    parser = argparse.ArgumentParser(
        prog="BiliExper",
        description='哔哩哔哩助手',
        epilog="注意：random参数不能大于looping参数，也不能大于多个tm参数间的时间间隔\n",
        add_help=False
    )
    parser.add_argument(
        '-h', '--help',
        action='help',
        help='帮助'
    )

    parser.add_argument(
        '-c', '--configfile',
        dest='configfile',
        help='配置文件路径'
    )
    parser.add_argument(
        '-l', '--logfile',
        dest='logfile',
        help='日志文件路径'
    )
    parser.add_argument(
        '-r', '--random',
        dest='random',
        type=int,
        nargs='?',
        const=300,
        help='随机延时范围，单位为秒，默认值为300'
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-lo','--looping',
        dest='looping',
        type=int,
        nargs='?',
        const=3600*24,
        help='循环运行间隔，使用此参数将开启循环运行，参数单位为秒（s），默认值为86400。与timing参数互斥'
    )
    group.add_argument(
        '-tm','--timing',
        dest='timing',
        action='append',
        type=convertTimeString,
        help='指定时间执行,如11:30:00，可以多次使用，如"-tm 11:30:00 -tm 16:00:00"。与looping参数互斥'
    )
    parser.add_argument(
        '-v','--version',
        action='version',
        version='%(prog)s {version}'.format(version=main_version_str),
        help="版本号"
    )
    parser.add_argument(
        '--debug',
        help="--debug TASK_FILE_NAME 调试单个 task",
    )

    args = parser.parse_args()
    if not isinstance(args, dict):
        args = vars(args)
    # await asyncio.create_task(main(args))
    main(args)