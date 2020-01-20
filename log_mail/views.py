from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
import json
from urllib import parse
from django.core.mail  import  send_mail
from django.core.mail import EmailMessage
from django.template import loader
from .util import kibana_mail,kibana_api
from ops_notfiy.settings import EMAIL_HOST_USER,KIBANA_URL,KIBANA_DATE_TIME,EMAIL_TO
class kibana_sentinal(View):
    def post(self,request):
        subject = u'日志报警系统'
        mes = dict()
        otherMes = dict()
        Errors = list()
        Mails = dict()
        messages = json.loads(request.body.decode('utf-8'))
        for AppLogs in messages:
            AppName = AppLogs['appName']
            for Logs in AppLogs["errors"]:
                Log = Logs['message'].replace('%u','\\u')
                bytes = parse.unquote_to_bytes(Log)
                bytes = bytes.decode('unicode-escape')
                # httpRef = "%s/app/kibana#/discover?_g=(refreshInterval:(pause:!t,value:0),time:(from:%s,mode:quick,to:now))&_a=(columns:!(_source),index:'22595e70-fb92-11e9-8a18-2b708bc20a0c',interval:auto,query:(language:lucene,query:'_id:%s'),sort:!('@timestamp',desc))" %(KIBANA_URL,KIBANA_DATE_TIME,Logs['id'])
                # httpRef = "%s/app/kibana#/doc/%s/%s/fluentd?id=%s&_g=(refreshInterval:(pause:!t,value:0),time:(from:%s,mode:quick,to:now))" %(KIBANA_URL,kibana_api.data,Logs['index'],Logs['id'],KIBANA_DATE_TIME)
                httpRef = "%s/app/kibana#/context/%s/%s/%s?_a=(columns:!(_source),filters:!(('$state':(store:appState),meta:(alias:!n,disabled:!f,index:'4fa5af10-0429-11ea-9ef8-019832b3e032',key:appname,negate:!f,params:(query:%s,type:phrase),type:phrase,value:%s),query:(match:(appname:(query:%s,type:phrase))))),predecessorCount:5,sort:!('@timestamp',desc),successorCount:5)&_g=(refreshInterval:(pause:!t,value:0),time:(from:%s,mode:quick,to:now))" %(KIBANA_URL,kibana_api.data,Logs['type'],Logs['id'],AppLogs['appName'],AppLogs['appName'],AppLogs['appName'],KIBANA_DATE_TIME)
                if len(bytes) > 150:
                    bytesLimit = bytes[0:150] + "......"
                    Errors.append({'message':bytes,'count':len(bytes),'bytesLimit':bytesLimit,'httpRef':httpRef})
                else:
                    Errors.append({'message':bytes,'count':len(bytes),'httpRef':httpRef})
            if AppName in EMAIL_TO:
                Mails[AppName] = EMAIL_TO[AppName]
                mes[AppName] = Errors

                if mes != {}:
                    html_content = loader.render_to_string(
                        'logs-mail.html', {
                            'user': Mails[AppName]['username'],
                            'messages': mes
                        }
                    )
                    kibana_mail.send_html_mail(subject, html_content, Mails[AppName]['mailto'])
            else:
                Mails['other'] = EMAIL_TO['other']
                otherMes[AppName] = Errors
        if otherMes != {}:
            html_other_content = loader.render_to_string(
                'logs-mail.html', {
                    'user': Mails['other']['username'],
                    'messages': otherMes
                }
            )
            kibana_mail.send_html_mail(subject, html_other_content, Mails['other']['mailto'])
        code = {'code': 200}
        return HttpResponse(json.dumps(code), content_type="application/json")
# Create your views here.
