import urllib.request
import urllib.parse
#请求头
headers = { 
	'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36",
	'Referer':'http://www.zhaokeli.com/'
		 }
#取网页数据
def geturl(url,data={}):
	try:
		params=urllib.parse.urlencode(data).encode(encoding='UTF8')
		req=urllib.request.Request("%s?%s"%(url, params))
		#设置headers
		for i in headers:
			req.add_header(i,headers[i])

		r=urllib.request.urlopen(req)
		html =r.read()
		return html
	except urllib.error.HTTPError as e:
	    print(e.code)
	    print(e.read().decode("utf8"))
	
def posturl(url,data={}):
	try:
		params=urllib.parse.urlencode(data).encode(encoding='UTF8')
		req = urllib.request.Request(url, params,headers)
		r = urllib.request.urlopen(req)
		html =r.read()
		return str(html)
	except urllib.error.HTTPError as e:
	    print(e.code)
	    print(e.read().decode("utf8"))

def toutf8(s):
	if(isinstance(s,bytes)):
		s.decode('utf-8')
	if(isinstance(s,str)):
		s.encode(encoding="utf-8").decode('utf-8')
	return s

