from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from . import views
urlpatterns = [
    url(r'logs/mail/error_logs_notify',views.kibana_sentinal.as_view())
]