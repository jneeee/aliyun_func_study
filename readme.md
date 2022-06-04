# 一个阿里云函数计算上手项目

## 参考

- [serverless-devs](https://www.serverless-devs.com)
- [189checkin](https://github.com/Cluas/189checkin)
- [aliyun.log SDK](http://aliyun-log-python-sdk.readthedocs.io/)
- [smzdm_sgin](https://github.com/myseil/smzdm_sgin)
- [Python pickling of objects into sqlite db](https://gist.github.com/JonathanRaiman/aa0bdfd8e3511c59f3af)


## todo
- ~~use aliyun.log(index, topic, ...)~~ 云函数的 stdout 和 logging 会自动储存到日志服务，所以这个属于脱裤子放屁。可以考虑实现 pull_log, ref [日志服务 Python sdk 示例](https://github.com/aliyun/aliyun-log-python-sdk/blob/master/tests/sample.py?spm=a2c4g.11186623.0.0.38f95c2a9X6i3c&file=sample.py)
- :white_check_mark: add task_runned flag to db;
- :white_check_mark: 大任务异步执行
- ~~抽奖改单次，不sleep(可以显著降低计算资源)~~
- :white_check_mark: ~~统一推送~~
- :white_check_mark: db.py 使用 pickle 读写 sqlite
