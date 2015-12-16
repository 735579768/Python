# Used information from:
# http://stackoverflow.com/questions/463832/using-dpapi-with-python
# http://www.linkedin.com/groups/Google-Chrome-encrypt-Stored-Cookies-36874.S.5826955428000456708

from ctypes import *
from ctypes.wintypes import DWORD
import sqlite3,os, chardet
import urllib.request
import http.cookiejar
LocalFree = windll.kernel32.LocalFree;
memcpy = cdll.msvcrt.memcpy;
CryptProtectData = windll.crypt32.CryptProtectData;
CryptUnprotectData = windll.crypt32.CryptUnprotectData;
CRYPTPROTECT_UI_FORBIDDEN = 0x01;
#谷歌cookies路径
chromeCookiesPath=os.path.join(os.environ['LOCALAPPDATA'], r'Google\Chrome\User Data\Default\Cookies')
headers = { 
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'
        } 
class DATA_BLOB(Structure):
    _fields_ = [("cbData", DWORD), ("pbData", POINTER(c_char))];

def getData(blobOut):
    cbData = int(blobOut.cbData);
    pbData = blobOut.pbData;
    buffer = c_buffer(cbData);
    memcpy(buffer, pbData, cbData);
    LocalFree(pbData);
    return buffer.raw;

def encrypt(plainText):
    bufferIn = c_buffer(plainText, len(plainText));
    blobIn = DATA_BLOB(len(plainText), bufferIn);   
    blobOut = DATA_BLOB();

    if CryptProtectData(byref(blobIn), u"python_data", None,
                       None, None, CRYPTPROTECT_UI_FORBIDDEN, byref(blobOut)):
        return getData(blobOut);
    else:
        raise Exception("Failed to encrypt data");

def decrypt(cipherText):
    bufferIn = c_buffer(cipherText, len(cipherText));
    blobIn = DATA_BLOB(len(cipherText), bufferIn);
    blobOut = DATA_BLOB();

    if CryptUnprotectData(byref(blobIn), None, None, None, None,
                              CRYPTPROTECT_UI_FORBIDDEN, byref(blobOut)):
        return getData(blobOut);
    else:
        raise Exception("Failed to decrypt data");

#取指定域名的cookies
def getChromeCookies(hostname):
	hostname="%{0}%".format(hostname);
	conn = sqlite3.connect(chromeCookiesPath);
	c = conn.cursor();
	c.execute("SELECT  host_key, name, path,value,encrypted_value FROM cookies WHERE host_key like '%{0}%';".format(hostname));
	cookies = c.fetchall();
	c.close();
	rearr=[]
	for row in cookies:
	    dc = decrypt(row[4]).decode('utf-8');
	    rearr.append({'name':row[1],'value':dc,'path':row[2],'hostname':row[0]})
#	    print( \
# 	"""
# host_key: {0}
# name: {1}
# path: {2}
# value: {3}
# encrpyted_value: {4}
# 	""".format(row[0], row[1], row[2], row[3], dc));
	return rearr
def build_opener_with_cookies(domain=None):
    #读入cookies
    cookiejar = http.cookiejar.MozillaCookieJar()    # No cookies stored yet
    arr=getChromeCookies(domain)
    
    for a in arr:
        cookie_item = http.cookiejar.Cookie(
            version=0, name=str(a['name']), value=str(a['value']),
                     port=None, port_specified=None,
                     domain=str(a['hostname']), domain_specified=None, domain_initial_dot=None,
                     path=str(a['path']), path_specified=None,
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
def geturlByChrome(url,data={},domain=''):
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
        return opener.open(req)
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read().decode())
        return False
    #get取网页数据
def posturlByChrome(url,data={},domain=''):
    opener=build_opener_with_cookies(domain)
    try:
        params=urllib.parse.urlencode(data).encode(encoding='UTF8')
        req=urllib.request.Request(url,params,headers)
        return opener.open(req) 
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read().decode("utf8"))
        return False;
if __name__ == '__main__':
#     cookies=getChromeCookies('',r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Profile 8\Cookies')
#     for row in cookies:
#         print( \
#  	"""
# hostname: {0}
# name: {1}
# path: {2}
# value: {3}
#  	""".format(row['hostname'], row['name'], row['path'], row['value']));
    chromeCookiesPath=r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Profile 8\Cookies'
    #r=geturlByChrome('https://uemprod.alipay.com/user/ihome.htm?enctraceid=hUOmUrNCsjIIix9qdYFUmm18P0SmJma19x-9MXcIAPA',{},'alipay.com')
    r=geturlByChrome('http://user.zhaokeli.com',{},'zhaokeli.com')
    if r != False:
        datatext=r.read()
        charset=chardet.detect(datatext)
        print(datatext.decode(charset['encoding']))
        #print(r.read().decode('gb2312'))
    else:
        print('fail')
    input('输入任意键继续...')
