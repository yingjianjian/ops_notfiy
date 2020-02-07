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


        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)',
            'Content-Type': 'application/json',
        }  # 定义头信息

        for alert in alerts:
            if alert['labels']['alertname'] == 'Watchdog':
                url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=20de74df-fdcf-4a56-a410-990155f9bfe2'
                userList = []
            else:
                url = PRO_URL
                userList = ["@all"]
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
            dict = {
                "msgtype": "markdown",
                "markdown": {
                    "content": content
                }
            }

            # data = bytes(parse.urlencode(dict), encoding='utf-8')
            req = requests.post(url,json=dict)
            # response = requEst.urlopen(req)
            # print(response)
            if userList != []:
                text = {
                    "msgtype": "text",
                    "text": {
                        "content": "%s出现报警 请查看！" % (alert['project']),
                        "mentioned_list": ["@all"]
                    }
                }
                requests.post(url, json=text)
        code = {'code': 200}
        return HttpResponse(json.dumps(code), content_type="application/json")
