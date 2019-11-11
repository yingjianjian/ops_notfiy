import json
from urllib.request import Request, urlopen
from kibana_sentinl_mail.settings import KIBANA_URL
url = "%s/api/saved_objects/_find?type=index-pattern&per_page=10000"  %(KIBANA_URL)
firefox_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
request = Request( url, headers=firefox_headers )
html = urlopen(request)
data = json.loads(str(html.read(),'utf-8'))['saved_objects'][0]['id']