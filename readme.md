# 一个阿里云函数计算上手项目
使用阿里云函数计算、NAS 文件系统，日志服务做的爬虫项目。
数据库是 sqlite ，放在 NAS 文件系统。(冷启动比较慢)
部署主要使用 serverless-devs，他是阿里开源的函数计算跨平台部署工具，现在各种厂商（阿里 腾讯 华为 百度都有函数计算，外面有Aws lambda、Azure Functions）的云计算产品都很类似，利用这个工具可以一次开发，到处部署，推荐😁

## 1 如何使用
应该不太容易拿来即用...大概过程是这样：

1. 安装[serverless-devs](https://docs.serverless-devs.com/serverless-devs/quick_start)
2. 添加需要的层(layer)
层是函数计算里用来管理函数运行依赖的方式 [构建层 - 阿里云文档](https://help.aliyun.com/document_detail/193057.html) 。
需要本地创建一个 python文件夹，把依赖装进去，然后打包上传：
```bash
mkdir python
pip instsall -t python/ requests rsa flask jinja2
zip -r python.zip python/
```
2022-8-21 09:58:07 发现阿里云函数现在可以在线编辑 `requirements.txt` 在线构建。[Link](https://fcnext.console.aliyun.com/cn-shanghai/layers)

3. 配置`s.yaml`，里面关于函数 layers 字段
4. 执行`s corntask develop`
5. 去网页或者用s工具调试

## 2 Todo
- [ ] Refact with apscheduler
- [ ] Acfun task
- [ ] ~~use aliyun.log(index, topic, ...)~~ 云函数的 stdout 和 logging 会自动储存到日志服务，所以这个属于脱裤子放屁。可以考虑实现 pull_log, ref [日志服务 Python sdk 示例](https://github.com/aliyun/aliyun-log-python-sdk/blob/master/tests/sample.py?spm=a2c4g.11186623.0.0.38f95c2a9X6i3c&file=sample.py)
- [x] add task_runned flag to db;
- [x] 大任务异步执行；
- ~~抽奖改单次，不sleep(可以显著降低计算资源)~~
- [x] ~~统一推送~~
- [x] db.py 做成kv存储，使用 pickle 读写 sqlite 文件

## 3 参考

- [serverless-devs](https://www.serverless-devs.com)
- [189checkin](https://github.com/Cluas/189checkin)
- [aliyun.log SDK](http://aliyun-log-python-sdk.readthedocs.io/)
- [smzdm_sgin](https://github.com/myseil/smzdm_sgin)
- [Python pickling of objects into sqlite db](https://gist.github.com/JonathanRaiman/aa0bdfd8e3511c59f3af)
- acfun 部分参考 [acfun.py - dailycheckin](https://github.com/Sitoi/dailycheckin/blob/b2f023f3e7acbbf2d64c2980c4bfa4623242a50c/acfun/acfun.py)(api过期很多) [banana-helper](https://github.com/zhuweitung/banana-helper)
