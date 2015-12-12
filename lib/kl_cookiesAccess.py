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
    conn.close()
def geturl(url,data={},domain=''):
    opener=build_opener_with_cookies(domain)
    try:
        params=urllib.parse.urlencode(data)#.encode(encoding='UTF8')
        req=''
        if params=='' :
               req=urllib.request.Request(url)
        else:
               req=urllib.request.Request(url+'?%s'%(params)) 
        
        #设置headers
        for i in headers:
            req.add_header(i,headers[i])
        req.add_header('Referer',url)
        r=opener.open(req)
        return r
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read().decode("utf8"))
        return opener.open(url)

if __name__ == '__main__':
    r = geturl(url='http://user.zhaokeli.com',domain='zhaokeli.com')
    #r = geturl(url='https://www.baidu.com/?tn=63090008_1_hao_pg',domain='baidu.com')
    s=r.read().decode()
    print(s)
    #conn.execute("insert into content(content) values(?)",(s,));
    #conn.commit()
    #conn.close()
    input('按任意键继续')
