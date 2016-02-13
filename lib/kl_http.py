'''
+----------------------------------------------------------------------
// | Author: 赵克立 <735579768@qq.com> <http://www.zhaokeli.com>
// |http数据库操作类
+----------------------------------------------------------------------
// | 自动保存请求中的cookies,
// | setcookies({})可以自定义cookies
// | setheaders({})自定义请求头信息
// |
// |
'''
import urllib.request,os, random,time
import urllib.parse
import http.cookiejar
import socket
socket.setdefaulttimeout(10)           #10秒内没有打开web页面，就算超时
useragent=[
'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
]
class kl_http:
    def __init__(self):
        self.lasterror=None
        self.proxy={
            'username':'',
            'password':'',
            'proxyserver':''
        }
        self.responsetime=0
        self.hostname=''
        self.headers = {}
        self.cookies = {}
        self.opener=None
        self.ckjar=None
        self.autoUserAgent=False

    #重置会话
    def resetsession(self):
        self.opener=None

    #设置cookies并创建会话
    def __setcookies(self,url):
        if   self.opener!=None:
            return None
        urls=urllib.parse.urlsplit(url)
        self.hostname=urls[1]
        if os.path.exists('./data/cookies')==False :
            os.makedirs('./data/cookies')

        #创建一个带cookie的网络打开器,后面的get post请求都使用这个打开
        self.ckjar=http.cookiejar.MozillaCookieJar("./data/cookies/cookies-%s.txt"%(self.hostname))
        try:
             """加载已存在的cookie，尝试此cookie是否还有效"""
             self.ckjar.load(ignore_discard=True, ignore_expires=True)
        except Exception:
             """加载失败，说明从未登录过，需创建一个cookie kong 文件"""
             self.ckjar.save(ignore_discard=True, ignore_expires=True)
        self.__addcookies()
        ckproc=urllib.request.HTTPCookieProcessor(self.ckjar)

        #代理
        if self.proxy['proxyserver']!='':
            proxy='http://%s:%s@%s' %(self.proxy['username'],self.proxy['password'],self.proxy['proxyserver'])
            proxy_handler=urllib.request.ProxyHandler({'http':proxy})
            self.opener=urllib.request.build_opener(ckproc,proxy_handler)
            return None

        self.opener=urllib.request.build_opener(ckproc)

    #添加自定义的cookies
    def __addcookies(self):
        for a, b in self.cookies.items():
            cookie_item = http.cookiejar.Cookie(
                version=0, name=a, value=b,
                         port=None, port_specified=None,
                         domain=self.hostname, domain_specified=None, domain_initial_dot=None,
                         path=r'/', path_specified=None,
                         secure=None,
                         expires=None,
                         discard=None,
                         comment=None,
                         comment_url=None,
                         rest=None,
                         rfc2109=False,
                )
            self.ckjar.set_cookie(cookie_item)    # Apply each cookie_item to cookiejar

    #设置代理服务器
    def setproxy(self,username,password,proxyserver):
        self.opener=None
        self.proxy['username']=username
        self.proxy['password']=password
        self.proxy['proxyserver']=proxyserver

    #设置请求的header头
    def setheaders(self,data):
        if type(data)==type(''):
            data=data.splitlines()
            for i in data:
                if i!="":
                    tem=i.split(':')
                    self.headers[tem[0]]=tem[1]
        elif type(data)==type({}):
            self.headers=data
        self.resetsession()

    def setcookies(self,data):
        if type(data)==type(''):
            data=data.split(';')
            for i in data:
                if i!='':
                    tem=i.split('=')
                    self.cookies[tem[0]]=tem[1]
        elif type(data)==type({}):
            self.cookies=data
        self.resetsession()

    #设置超时
    def settimeout(self,timeout=10):
        socket.setdefaulttimeout(timeout)

    #get取网页数据
    def geturl(self,url,data={}):
            global useragent
            self.__setcookies(url)
            r=None
            try:
                params=urllib.parse.urlencode(data)#.encode(encoding='UTF8')
                req=''
                if params=='' :
                       req=urllib.request.Request(url)
                else:
                       req=urllib.request.Request(url+'?%s'%(params))

                #设置headers
                for a,b in self.headers.items():
                    req.add_header(a,b)
                req.add_header('Referer',url)
                if self.autoUserAgent:
                    usag=random.randint(0,18)
                    req.add_header('User-Agent',useragent[usag]);
                starttime=time.time()
                r=self.opener.open(req)
                self.responsetime=time.time()-starttime
                self.ckjar.save(ignore_discard=True, ignore_expires=True)
                return r
            except urllib.error.HTTPError as e:
                #print(e.code)
                self.lasterror=e
                return r
            except urllib.error.URLError as e:
                #print(e.reason)
                self.lasterror=e
                return r
            except:
                return r

    #get取网页数据
    def posturl(self,url,data={}):
        global useragent
        self.__setcookies(url)
        r=None
        try:
            params=urllib.parse.urlencode(data).encode(encoding='UTF8')
            req=urllib.request.Request(url,params,self.headers)
            req.add_header('Referer',url)

            if self.autoUserAgent:
                usag=random.randint(0,18)
                req.add_header('User-Agent',useragent[usag]);
            starttime=time.time()
            r=self.opener.open(req)
            self.responsetime=time.time()-starttime
            self.ckjar.save(ignore_discard=True, ignore_expires=True)
            return r
        except urllib.error.HTTPError as e:
            #print(e.code)
            self.lasterror=e
            return r
        except urllib.error.URLError as e:
            #print(e.reason)
            self.lasterror=e
            return r
        except:
            return r

if __name__ == '__main__':
    ht=kl_http()
    ht.setheaders('''\
Accept:*/*
Accept-Language:en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2
User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36\
    ''');
    ht.setcookies('ankc_admin__uid__=ainiku%3A%7B%22u%22%3A%22MDAwMDAwMDAwMLyQiNbHupWh%22%2C%22p%22%3A%22MDAwMDAwMDAwMLyQiNbHupbdxGRqlcaUqHU%22%7D;')
    ht.setproxy('','','127.0.0.1:8087')
    #r=ht.posturl(r'http://127.0.0.1/')
    r=ht.posturl(r'http://1212.ip138.com/ic.asp').read().decode('gb2312')
    print(r)
    input('按任意键继续...')
