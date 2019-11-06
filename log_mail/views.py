from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
import json
from urllib import parse
from django.core.mail  import  send_mail
from django.core.mail import EmailMessage
from django.template import loader
from kibana_sentinl_mail.settings import EMAIL_HOST_USER,KIBANA_URL,KIBANA_DATE_TIME,EMAIL_TO
from .util import kibana_mail
class kibana_sentinal(View):
    def post(self,request):
        subject = u'日志报警系统'
        mes = dict()
        Errors = list()
        messages = json.loads(request.body.decode('utf-8'))
        for AppLogs in messages:
            AppName = AppLogs['appName']
            for Logs in AppLogs["errors"]:
                Log = Logs['message'].replace('%u','\\u')
                bytes = parse.unquote_to_bytes(Log)
                bytes = bytes.decode('unicode-escape')
                # httpRef = "%s/app/kibana#/discover?_g=(refreshInterval:(pause:!t,value:0),time:(from:%s,mode:quick,to:now))&_a=(columns:!(_source),index:'22595e70-fb92-11e9-8a18-2b708bc20a0c',interval:auto,query:(language:lucene,query:'_id:%s'),sort:!('@timestamp',desc))" %(KIBANA_URL,KIBANA_DATE_TIME,Logs['id'])
                httpRef = "%s/app/kibana#/doc/22595e70-fb92-11e9-8a18-2b708bc20a0c/%s/fluentd?id=%s&_g=(refreshInterval:(pause:!t,value:0),time:(from:%s,mode:quick,to:now))" %(KIBANA_URL,Logs['index'],Logs['id'],KIBANA_DATE_TIME)
                if len(bytes) > 150:
                    bytesLimit = bytes[0:150] + "......"
                    Errors.append({'message':bytes,'count':len(bytes),'bytesLimit':bytesLimit,'httpRef':httpRef})
                else:
                    Errors.append({'message':bytes,'count':len(bytes),'httpRef':httpRef})
            mes[AppName] = Errors
            if AppName in EMAIL_TO:
                Mails = EMAIL_TO[AppName]
            else:
                Mails = EMAIL_TO['other']
            html_content = loader.render_to_string(
                'logs-mail.html', {
                    'user': Mails['username'],
                    'messages': mes
                }
            )
            kibana_mail.send_html_mail(subject,html_content,Mails['mailto'])
        code = {'code': 200}
        return HttpResponse(json.dumps(code), content_type="application/json")
# Create your views here.
