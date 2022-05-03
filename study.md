发布层layer (公共依赖)，在s project路径下执行
```shell
mkdir -p code/python
pip install flask -t code/python
pip install requests rsa -t code/python
s next-function layer publish --layer-name flask_requests_rsa --code ./code/
```
python 还需要注意的是包需要放在 ./code/python/ 路径下
