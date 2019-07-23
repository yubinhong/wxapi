import json
import redis
import requests
from wb_wx import settings
from api import models


def wxapi(user, party_id, agent_id, content, corp_name):
    token = gettoken(agent_id, corp_name)
    if token == '':
        message = "Get token is failed!"
        return message
    url = settings.WX_API % token
    data = {
        "touser": user,
        "toparty": party_id,
        "msgtype": "text",
        "agentid": agent_id,
        "text": {
            "content": content
        },
        "safe": "0"
    }
    try:
        r = requests.post(url=url, data=json.dumps(data), verify=False, timeout=5)
    except Exception as e:
        print(e)
        return str(e)
    return r.text


def gettoken(agent_id, corp_name):
    corpobj = models.Corp.objects.get(corp_name=corp_name)
    corpid = corpobj.corp_id
    redis_client = redis.Redis(**settings.REDIS_CONFIG)
    if redis_client.exists("token:%s:%s" % (corpid, agent_id)):
        token = redis_client.get("token:%s:%s" % (corpid, agent_id))
    else:
        agentobj = models.Agent.objects.get(agent_id=agent_id, corp=corpobj)
        corpsecret = agentobj.corp_secret
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        data = {
            "corpid": corpid,
            "corpsecret": corpsecret
        }
        try:
            r = requests.get(url=url, params=data, verify=False, timeout=5)
            print(r.content)
            token = r.json()['access_token']
            redis_client.setex("token:%s:%s" % (corpid, agent_id), 5400, token)
        except Exception as e:
            print(e)
            token = ''
    return token


def exist_secret(agent_id, corp_name):
    corpobj = models.Corp.objects.get(corp_name=corp_name)
    if len(models.Agent.objects.filter(agent_id=agent_id, corp=corpobj)):
        return 1
    else:
        return 0

