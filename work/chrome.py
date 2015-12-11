import os
import sqlite3
import urllib.request
import http.cookiejar
#C:\Users\KELI\AppData\Local\Google\Chrome\User Data\Default\Cookies
def build_opener_with_chrome_cookies(domain=None):
    cookie_file_path = os.path.join(os.environ['LOCALAPPDATA'], r'Google\Chrome\User Data\Default\Cookies')
    cookie_file_path = r'C:\Users\KELI\AppData\Local\Google\Chrome\User Data\Default\Cookies'
    if not os.path.exists(cookie_file_path):
        raise Exception('Cookies file not exist!')
    conn = sqlite3.connect(cookie_file_path)
    sql = 'select host_key, name, value, path from cookies'
    if domain:
        sql += ' where host_key like "%{}%"'.format(domain)
        
    cookiejar = http.cookiejar.MozillaCookieJar()    # No cookies stored yet

    for row in conn.execute(sql):
        print(row[1],row[2])
        cookie_item = http.cookiejar.Cookie(
            version=0, name=row[1], value=row[2],
                     port=None, port_specified=None,
                     domain=row[0], domain_specified=None, domain_initial_dot=None,
                     path=row[3], path_specified=None,
                     secure=None,
                     expires=None,
                     discard=None,
                     comment=None,
                     comment_url=None,
                     rest=None,
                     rfc2109=False,
            )
        cookiejar.set_cookie(cookie_item)    # Apply each cookie_item to cookiejar
    
    #return urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))    # Return opener
    ckproc=urllib.request.HTTPCookieProcessor(cookiejar)
    opener=urllib.request.build_opener(ckproc)
    return opener
    conn.close()


if __name__ == '__main__':
    
    opener = build_opener_with_chrome_cookies(domain='zhaokeli.com')
    html_doc = opener.open('http://user.zhaokeli.com/index.php?m=Admin&c=Archive&a=index&model_id=1&mainmenu=true').read()
    import re
    #print(html_doc.decode())
    #print ('Title:', re.search('<title>(.*?)</title>', html_doc, re.IGNORECASE).group(1))
