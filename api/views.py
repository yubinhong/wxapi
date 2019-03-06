# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import time
from backend import wxApi
from backend import secure

from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@csrf_exempt
def send_message(request):
    data = {}
    if request.method != 'POST':
        data['message'] = "The method should be POST"
        data['code'] = "300001"
        data = json.dumps(data)
        return HttpResponse(data)
    else:
        from_json = False
        if request.content_type == 'application/json':
            receive_data = json.loads(request.body)
            from_json = True
            try:
                user = receive_data['user']
            except Exception as e:
                receive_data['user'] = ''
            try:
                party = receive_data['party']
            except Exception as e:
                receive_data['party'] = ''

            try:
                corp_name = receive_data['corp_name']
            except Exception as e:
                receive_data['corp_name'] = ''

        user = receive_data['user'] if from_json else request.POST.get('user', '')
        party = receive_data['party'] if from_json else request.POST.get('party', '')
        agent_id = int(receive_data['agent_id']) if from_json else int(request.POST.get('agent_id', ''))
        content = receive_data['content'] if from_json else request.POST.get('content', '')
        current_time = int(time.time())
        receive_time = int(receive_data['time']) if from_json else int(request.POST.get('time'))
        signature = receive_data['signature'] if from_json else request.POST.get('signature')
        corp_name = receive_data['corp_name'] if from_json else request.POST.get('corp_name', '')
        less_time = current_time - receive_time
        exist = wxApi.exist_secret(agent_id, corp_name)

        if signature != secure.to_secure(receive_time) or less_time > 300:
            data['message'] = "The param signature is not valid"
            data['code'] = "300002"
            data = json.dumps(data)
            return HttpResponse(data)
        if user == '' and party == '':
            data['message'] = "The param user and party would not null at the same time"
            data['code'] = '300003'
            data = json.dumps(data)
            return HttpResponse(data)
        if content == '':
            data['message'] = "The param content would not null"
            data['code'] = "300004"
            data = json.dumps(data)
            return HttpResponse(data)
        if corp_name == '':
            data['message'] = "The param corp_name would not null"
            data['code'] = "300008"
            return HttpResponse(json.dumps(data))
        if agent_id == '':
            data['message'] = "The param agent_id would not null"
            data['code'] = "300009"
            return HttpResponse(json.dumps(data))
        if exist == 0:
            data['message'] = "The corpsecret is not exists"
            data['code'] = "300007"
            data = json.dumps(data)
            return HttpResponse(data)
        return HttpResponse(wxApi.wxapi(user, party, agent_id, content, corp_name))




