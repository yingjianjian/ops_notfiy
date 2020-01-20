from django.shortcuts import render
from django.views.generic import View
import json
from django.http import HttpResponse
from . import util
import requests
import datetime
from ops_notfiy.settings import PRO_PROJECT,PRO_URL
# Create your views here.

class prometheusWebhook(View):
    def __india_to_local(self, india_time_str, india_format='%Y-%m-%dT%H:%M:%S.%fZ'):
        india_dt = datetime.datetime.strptime(india_time_str, india_format)
        local_dt = india_dt + datetime.timedelta(hours=8)
        local_format = "%Y-%m-%d %H:%M:%S"
        time_str = local_dt.strftime(local_format)
        return time_str

    def post(self,request):
        messages = json.loads(request.body.decode('utf-8'))
        status = messages['status']
        alerts = messages['alerts']
        url = PRO_URL
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)',
            'Content-Type': 'application/json',
        }  # 定义头信息

        for alert in alerts:
            if alert['status'] == 'resolved':
                alert['status'] = "<font color='info'>`已解决`</font>"
                alert['project'] = PRO_PROJECT
                content = """
报警状态:%s
>**项目名**

%s

>
>**报警详情**
%s
>
>**描述**
%s 
>**报警时间**

%s

>**恢复时间**

%s
                            """ % (alert['status'],alert['project'], util.rep_str(alert['labels']), util.rep_str(alert['annotations']),
                                   self.__india_to_local(alert['startsAt'][:-4] + 'Z'),
                                   self.__india_to_local(alert['endsAt'][:-4] + 'Z'))
            elif alert['status'] == 'firing':
                alert['status'] = "<font color='error'>`报警中`</font>"
                alert['project'] = PRO_PROJECT
                content = """
报警状态:%s
>**项目名**

%s

>
>**报警详情**
%s
>
>**描述**
%s 
>**报警时间**

%s
                """%(alert['status'],alert['project'],util.rep_str(alert['labels']),util.rep_str(alert['annotations']),self.__india_to_local(alert['startsAt'][:-4]+'Z'))
            # print(content)
            print(alert['startsAt'][:-4]+'Z')
            dict = {
                "touser": "UserID1|UserID2|UserID3",
                "toparty": "PartyID1|PartyID2",
                "totag": "TagID1 | TagID2",
                "msgtype": "markdown",
                "agentid": 1,
                "markdown": {
                    "content": content
                },
                "enable_duplicate_check": 0
            }
            print(dict)
            # data = bytes(parse.urlencode(dict), encoding='utf-8')
            req = requests.post(url,json=dict)
            # response = requEst.urlopen(req)
            # print(response)
        code = {'code': 200}
        return HttpResponse(json.dumps(code), content_type="application/json")
