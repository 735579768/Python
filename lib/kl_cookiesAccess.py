'''
从文件中读取cookies访问网页
'''
import os,sys
import sqlite3
import urllib.request
import http.cookiejar

datafile='./data/cookiesAccess/da.db'
datapath='./data/cookiesAccess'
if os.path.exists(datapath)==False :
    os.makedirs(datapath)
conn = sqlite3.connect(datafile)
def build_opener_with_cookies(domain=None):
    #读入cookies
    try:
        f=open(datapath+'/cookiesAccess.txt','r');
        s=f.read()
        f.close()
    except:
        print (datapath+'/cookiesAccess.txt is not exist!')
        input('按任意键继续')
        sys.exit(-1)
    cookiejar = http.cookiejar.MozillaCookieJar()    # No cookies stored yet
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
def geturl(url,domain):
    opener=build_opener_with_cookies(domain)
    return opener.open(url)

if __name__ == '__main__':
    r = geturl(url='http://user.zhaokeli.com',domain='zhaokeli.com')
    s=r.read().decode()
    print(s)
    conn.execute("insert into content(content) values(?)",(s,));
    conn.commit()
    conn.close()
    input('按任意键继续')
