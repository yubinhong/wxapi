import requests
import hashlib
import time
def main():
    url="http://127.0.0.1:8000/api/v2/alert"
    data = {}
    data['corp_name'] = 'WB'
    data['user']='Yubinhong'
    #data['party']='7'
    data['agent_id']='1000006'
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
