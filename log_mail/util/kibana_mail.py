# -*- coding: utf-8 -*-
from django.core.mail import EmailMessage
from django.template import loader

from kibana_sentinl_mail.settings import EMAIL_HOST_USER  # 项目配置邮件地址，请参考发送普通邮件部分


def send_html_mail(subject, html_content, recipient_list):
    msg = EmailMessage(subject, html_content, EMAIL_HOST_USER, recipient_list)
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()



