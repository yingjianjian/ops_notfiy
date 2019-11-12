"kibana-sentinl-mail" 

使用kibana Sentinl webhook 实现日志报警功能

Sentin-config 为kibana Sentinl的配置文件

安装依赖包
pip3 install -r requirements.txt

启动：

先设置环境变量：

EMAIL_HOST：SMTP服务地址：默认值：smtp.exmail.qq.com

EMAIL_PORT： SMTP 端口： 默认值：465

EMAIL_HOST_USER： 发件人邮箱

EMAIL_HOST_PASSWORD： 邮箱登录密码

EMAIL_USE_SSL： 是否开启HTTPS  默认为True

EMAIL_FROM： 邮件别名

KIBANA_URL： kibana的URL地址

KIBANA_DATE_TIME： kibana查询时间范围默认now-1h

EMAIL_TO 类型为JSON 串 在setting.py里设置，key为项目名，value为json类型 key为名称，value为邮箱地址
 设置方法例如：
export EMAIL_HOST=smtp.exmail.qq.com

python3 manager runserver 192.168.10.190:8002
 
 