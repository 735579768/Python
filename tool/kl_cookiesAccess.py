'''
从文件中读取cookies访问网页
'''
import os,sys
import sqlite3
import urllib.request
import http.cookiejar

headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'
        }
datafile='./data/cookiesAccess/da.db'
datapath='./data/cookiesAccess'
if os.path.exists(datapath)==False :
    os.makedirs(datapath)
#conn = sqlite3.connect(datafile)
#创建一个会话对象
def build_opener_with_cookies(domain=None):
    #读入cookies
    s=''
    try:
        f=open(datapath+'/'+domain+'-cookiesAccess.txt','r');
        s=f.read()
        f.close()
    except:
        f=open(datapath+'/'+domain+'-cookiesAccess.txt','w');
        f.close();
        print (datapath+'/'+domain+'-cookiesAccess.txt is empty!')

    cookiejar = http.cookiejar.MozillaCookieJar()    # No cookies stored yet
    if(s!=''):
        arr=s.split(';')
        for i in arr:
            if i!='':
                a=i.split('=')
                cookie_item = http.cookiejar.Cookie(
                    version=0, name=a[0], value=a[1],
                             port=None, port_specified=None,
                             domain=domain, domain_specified=None, domain_initial_dot=None,
                             path=r'/', path_specified=None,
                             secure=None,
                             expires=None,
                             discard=None,
                             comment=None,
                             comment_url=None,
                             rest=None,
                             rfc2109=False,
                    )
                cookiejar.set_cookie(cookie_item)    # Apply each cookie_item to cookiejar
    ckproc=urllib.request.HTTPCookieProcessor(cookiejar)
    opener=urllib.request.build_opener(ckproc)
    return opener

#请求一个页面
def geturl(url,data={},domain=''):
    opener=build_opener_with_cookies(domain)
    try:
        params=urllib.parse.urlencode(data)#.encode(encoding='UTF8')
        req=''
        if params=='' :
               req=urllib.request.Request(url)
        else:
               req=urllib.request.Request(url+'?%s'%(params))
        s=''
        try:
            f=open(datapath+'/'+domain+'-headerAccess.txt','r');
            s=f.read()
            f.close()
        except:
            f=open(datapath+'/'+domain+'-headerAccess.txt','w');
            f.close();
            print (datapath+'/'+domain+'-headerAccess.txt is empty!')
        
        if(s!=''):
            arr=s.split('\n')
            for i in arr:
                if i!='':
                    a=i.split(':')
                    req.add_header(a[0],a[1])
        else:
            for i in headers:
                req.add_header(i,headers[i])
        #设置headers

        req.add_header('Referer',url)
        r=opener.open(req)
        return r
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read().decode("utf8"))
        return opener.open(url)

if __name__ == '__main__':
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'
        }
    try:
        #r = geturl(url='http://user.zhaokeli.com',domain='zhaokeli.com')
        #r = geturl(url='http://user.nipic.com/',domain='nipic.com')
        #查看空间访客
        r = geturl(url='http://m.qzone.com/mqz_get_visitor?g_tk=1170550145&res_mode=0&res_uin=735579768&offset=0&count=10&page=1&format=json',domain='qzone.qq.com')
        
        #r = geturl(url='https://www.baidu.com/?tn=63090008_1_hao_pg',domain='baidu.com')
        #r = geturl(url='https://kyfw.12306.cn/otn/resources/js/framework/station_name.js',domain='kyfw.12306.cn')
        s=r.read().decode()
        print(s)
    except Exception as ex:
        print (Exception,":",ex)
    #conn.execute("insert into content(content) values(?)",(s,));
    #conn.commit()
    #conn.close()
    input('按任意键继续')
