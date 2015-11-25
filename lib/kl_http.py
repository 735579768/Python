import urllib.request
import urllib.parse
import http.cookiejar
class http:


    def __init__(self):
        #self.count = c;  
        #self.__class__.count = self.__class__.count + 1;
        self.headers = { 
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36',
        'Referer':'http://user.zhaokeli.com/'
        } 
        self.opener=None
        self.ckjar=None
        #创建一个带cookie的网络打开器,后面的get post请求都使用这个打开
        self.ckjar=http.cookiejar.MozillaCookieJar('cookies.txt')
        try:
             """加载已存在的cookie，尝试此cookie是否还有效"""
             self.ckjar.load(ignore_discard=True, ignore_expires=True)
        except Exception:
             """加载失败，说明从未登录过，需创建一个cookie kong 文件"""
             self.ckjar.save(ignore_discard=True, ignore_expires=True)
        ckproc=urllib.request.HTTPCookieProcessor(self.ckjar)
        self.opener=urllib.request.build_opener(ckproc)

    #get取网页数据
    def geturl(self,url,data={}):
            try:
                params=urllib.parse.urlencode(data)#.encode(encoding='UTF8')
                req=''
                if params=='' :
                       req=urllib.request.Request(url)
                else:
                       req=urllib.request.Request(url+'?%s'%(params)) 
                
                #设置headers
                for i in self.headers:
                    req.add_header(i,self.headers[i])
                r=self.opener.open(req)
                self.ckjar.save(ignore_discard=True, ignore_expires=True)
                return r
            except urllib.error.HTTPError as e:
                print(e.code)
                print(e.read().decode("utf8"))
            
    #get取网页数据
    def posturl(self,url,data={}):
        try:
            params=urllib.parse.urlencode(data).encode(encoding='UTF8')
            req=urllib.request.Request(url,params,self.headers)
            r=self.opener.open(req)
            self.ckjar.save(ignore_discard=True, ignore_expires=True)
            return r  
        except urllib.error.HTTPError as e:
            print(e.code)
            print(e.read().decode("utf8"))

            
if __name__ == '__main__':
	ht=http()
	print(ht.posturl(r'http://www.0yuanwang.com').read().decode())
	input('按任意键继续...')
