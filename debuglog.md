HTTP tigger evirsion
```
    '''{'LD_LIBRARY_PATH': '/code/:/code//lib:/usr/local/lib', 
    'SIGMA_APP_NAME': 'fn-', 
    'LANG': 'C.UTF-8', 
    'RUST_LOG': 'info', 
    'FC_FUNCTION_MEMORY_SIZE': '128', 
    'PYTHONIOENCODING': 'utf-8:surrogateescape',
    'FC_FUNC_CODE_PATH': '/code/',
    'PWD': '/code', 
    'HOME': '/tmp', 
    'TERM': 'xterm', 
    'PYTHON_VERSION': '3.9.8', 
    'SHLVL': '0', 
    'FC_RUNTIME_VERSION': '0.97.0', 
    'PATH': '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/var/fc/lang/python3.9/bin', 
    'KATA_CONTAINER': 'true', 
    'CONTENT_LENGTH': '0', 
    'HTTP': 'on', 
    'SCRIPT_NAME': '', 
    'SERVER_NAME': 'FCRUNTIME', 
    'SERVER_PORT': '9000', 
    'SERVER_PROTOCOL': 'HTTP/1.1', 
    'SERVER_SOFTWARE': 'FCRUNTIME/1.0', 
    'CONTENT_TYPE': 'application/octet-stream', 
    'QUERY_STRING': '', 
    'wsgi.version': (1, 0), 
    'wsgi.input': <_io.BytesIO object at 0x7f8e48230180>, 
    'wsgi.errors': <__main__.AsFlushWriter object at 0x7f8e48b17520>, 
    'wsgi.url_scheme': 'http', 
    'wsgi.multithread': False, 
    'wsgi.multiprocess': False, 
    'wsgi.run_once': False, 
    'PATH_INFO': '/', 
    'REQUEST_METHOD': 'GET', 
    'fc.request_uri': '/', 
    'REMOTE_ADDR': '211.161.243.70', 
    'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 
    'HTTP_ACCEPT_LANGUAGE': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6', 'HTTP_HOST': 'xxxxx', 
    'HTTP_SEC_CH_UA': '" Not A;Brand";v="99", 
    "Chromium";v="101", "Microsoft Edge";v="101"', 
    'HTTP_SEC_CH_UA_MOBILE': '?0', 
    'HTTP_SEC_CH_UA_PLATFORM': '"Windows"', 
    'HTTP_SEC_FETCH_DEST': 'document', 
    'HTTP_SEC_FETCH_MODE': 'navigate', 
    'HTTP_SEC_FETCH_SITE': 'cross-site', 
    'HTTP_SEC_FETCH_USER': '?1', 
    'HTTP_UPGRADE_INSECURE_REQUESTS': '1', 
    'HTTP_USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32', 
    'HTTP_X_FORWARDED_PROTO': 'https', 
    'HTTP_X_FC_FUNCTION_HANDLER': 'index.handler', 
    'fc.context': <fc_rapis_context.FCContext object at 0x7f8e47d100a0>}
    '''
```


原生 logging 在日志服务的内容：
```
serviceName:BiliExp
functionName:crontask
instanceID:c-627ec42d-de6aecb79ea04306bb44
message:2022-05-13T20:49:00.195Z 747b3ae9-3dc4-489a-9d7b-a2728751f2ac [INFO] 李杰米: 参与(生活改造计划·第三期 6.30)活动第(1/1)次，结果为(未中奖0)
qualifier:LATEST
versionId:
```
__topic__: BiliExp 
