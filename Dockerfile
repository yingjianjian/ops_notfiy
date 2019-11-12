FROM python:3.7-alpine
MAINTAINER 429795337@qq.com
WORKDIR /opt
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
    && apk add tzdata && apk add git && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && apk del tzdata
ADD .  /opt/
RUN apk add --no-cache  python3-dev gcc libc-dev
RUN mkdir -p /logs/
RUN pip install -r requriments.txt -i http://pypi.douban.com/simple  --trusted-host pypi.douban.com
EXPOSE 8002
CMD ['python3','manage.py','runserver','0:8002']
