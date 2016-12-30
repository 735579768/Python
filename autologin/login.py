import urllib.request
import urllib.parse
import http.cookiejar
import codecs
#请求头
headers = {
	'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36',
	'Referer':'http://user.zhaokeli.com/'#,
        #'X-Requested-With':'XMLHttpRequest'
	}
#创建一个带cookie的网络打开器,后面的get post请求都使用这个打开
ckjar=http.cookiejar.MozillaCookieJar('cookies.txt')
try:
     """加载已存在的cookie，尝试此cookie是否还有效"""
     ckjar.load(ignore_discard=True, ignore_expires=True)
except Exception:
     """加载失败，说明从未登录过，需创建一个cookie kong 文件"""
     ckjar.save(ignore_discard=True, ignore_expires=True)

ckproc=urllib.request.HTTPCookieProcessor(ckjar)
opener=urllib.request.build_opener(ckproc)
#get取网页数据
def geturl(url,data={}):
        try:
            global headers
            global opener
            params=urllib.parse.urlencode(data)#.encode(encoding='UTF8')
            req=''
            if params=='' :
                   req=urllib.request.Request(url)
            else:
                   req=urllib.request.Request(url+'?%s'%(params))

            #设置headers
            for i in headers:
                req.add_header(i,headers[i])
            r=opener.open(req)
            ckjar.save(ignore_discard=True, ignore_expires=True)
            return r
        except urllib.error.HTTPError as e:
            print(e.code)
            print(e.read().decode("utf8"))

#get取网页数据
def posturl(url,data={}):
    try:
        global headers
        global opener
        params=urllib.parse.urlencode(data).encode(encoding='UTF8')
        req=urllib.request.Request(url,params,headers)
        r=opener.open(req)
        ckjar.save(ignore_discard=True, ignore_expires=True)
        return r
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read().decode("utf8"))

da={'username':'','password':''}
loginurl=''
r=geturl(loginurl,{})
s1="%s"%r.read().decode()
#下面特征说明登陆成功
islogin=s1.find('登录成功')
islogin=s1.find('修改密码')
if islogin==-1 :
        #下载验证码
        f2 = open( r'./verify.png', 'wb' )
        urlSuning='http://user.zhaokeli.com/index.php'
        f2.write(geturl(urlSuning,{'m':'Admin','c':'Public','a':'verify'}).read())
        f2.close()
        da['verify']=input('请输入验证码:')
        r=posturl(loginurl,da)
        s1="%s"%r.read().decode()
        #下面特征说明登陆成功
        islogin=s1.find('登录成功')
        islogin=s1.find('修改密码')


while islogin==-1 :
    r=geturl(loginurl,{})
    #print(r.read().decode())
    #下载验证码
    f2 = open( r"./verify.png", "wb" )
    f2.write(geturl(urlSuning,{'m':'Admin','c':'Public','a':'verify'}).read())
    f2.close()
    print('验证码错误!')
    da['verify']=input('请输入验证码:')

    r=posturl(loginurl,da)
    s1="%s"%r.read().decode()
    #print(s1)
    islogin=s1.find('登录成功')

print('登陆成功')
input('请输入任意键继续...')
