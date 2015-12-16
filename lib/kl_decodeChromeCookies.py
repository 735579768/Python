# Used information from:
# http://stackoverflow.com/questions/463832/using-dpapi-with-python
# http://www.linkedin.com/groups/Google-Chrome-encrypt-Stored-Cookies-36874.S.5826955428000456708

from ctypes import *
from ctypes.wintypes import DWORD
import sqlite3;
LocalFree = windll.kernel32.LocalFree;
memcpy = cdll.msvcrt.memcpy;
CryptProtectData = windll.crypt32.CryptProtectData;
CryptUnprotectData = windll.crypt32.CryptUnprotectData;
CRYPTPROTECT_UI_FORBIDDEN = 0x01;

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
def getCookies(hostname,filepath):
	hostname="%zhaokeli.com%";
	conn = sqlite3.connect(filepath);
	c = conn.cursor();
	c.execute("SELECT  host_key, name, path,value,encrypted_value FROM cookies WHERE host_key like '%{0}%';".format(hostname));
	cookies = c.fetchall();
	c.close();
	rearr=[]
	for row in cookies:
	    dc = decrypt(row[4]);
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
if __name__ == '__main__':
    cookies=getCookies('zhaokeli.com',r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Profile 8\Cookies')
    for row in cookies:
        print( \
 	"""
hostname: {0}
name: {1}
path: {2}
value: {3}
 	""".format(row['hostname'], row['name'], row['path'], row['value']));
    input('输入任意键继续...')
