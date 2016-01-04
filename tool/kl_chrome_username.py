'''
使用谷歌cookies发起请求
'''
from ctypes import *
from ctypes.wintypes import DWORD
import sqlite3,os,sys, chardet
import urllib.request
import http.cookiejar
LocalFree = windll.kernel32.LocalFree;
memcpy = cdll.msvcrt.memcpy;
CryptProtectData = windll.crypt32.CryptProtectData;
CryptUnprotectData = windll.crypt32.CryptUnprotectData;
CRYPTPROTECT_UI_FORBIDDEN = 0x01;
#谷歌cookies路径
chromeCookiesPath=''
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
def getChromeUsername():
    global chromeCookiesPath
    if chromeCookiesPath=='':
        chromeCookiesPath=os.path.join(os.environ['LOCALAPPDATA'], r'Google\Chrome\User Data\Default\Login Data')
    if os.path.exists(chromeCookiesPath)==False :
        print("Chrome Logins file is not exist!:%s"%(chromeCookiesPath))
        sys.exit(0)
    conn = sqlite3.connect(chromeCookiesPath);
    c = conn.cursor();
    c.execute("SELECT  origin_url, action_url, username_element,username_value,password_element,password_value,form_data FROM logins ;");
    username = c.fetchall();
    c.close();
    return username
    '''
    rearr=[]
    for row in username:
        dc = decrypt(row[5]).decode('utf-8');
       # dc1 = decrypt(row[6]).decode('utf-8');
        rearr.append({'url':row[0],'password_value':dc, 'form_data':''})
    return rearr
    '''
if __name__ == '__main__':
    filepath='./data/username.csv'
    if os.path.exists(os.path.dirname(filepath))==False :
        os.makedirs(os.path.dirname(filepath))
    f=open(filepath,'w', encoding='utf-8')
    r=getChromeUsername()
    if r != False:
        for i in r:
            dc = decrypt(i[5]).decode('utf-8');
            f.write("%s,%s,%s,%s,%s,%s \n"%(i[0],i[1],i[2],i[3],i[4],dc))
            
    else:
        print('fail')
    f.close()
    input('chrome浏览器用户名密码导出完毕,输入任意键继续...')
