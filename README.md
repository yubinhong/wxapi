# wxapi
封装企业微信api

# 安装
pip install -r requirements.txt
## centos7
yum install redis
## ubuntu
apt-get install redis

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser

# 使用
## 1.登录后台http://127.0.0.1:8000/admin
## 2.添加企业信息以及应用id等信息
## 3.示例代码
```
import requests
import hashlib
import time
def main():
    url="http://127.0.0.1:8000/api/v2/alert"
    data = {}
    data['corp_name'] = 'test'
    data['user']='a'
    #data['party']='7'
    data['agent_id']='1000001'
    data['content']="Hello, this is wx_test"
    current_time=int(time.time())
    data['time']='%s' % current_time
    secure_word='KM1yeVcFbrL44ZGv' + '%s' % current_time
    s=hashlib.md5()
    s.update(secure_word.encode(encoding='utf-8'))
    data['signature']=s.hexdigest()
    req=requests.post(url, data=data)
    print(req.content)
if __name__=='__main__':
   main()
```
