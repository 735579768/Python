'''
查询品牌
'''
import kl_http,kl_db,os,json,kl_log
from postdata import postdata
http=kl_http.kl_http()
log=kl_log.kl_log('brand')
db=kl_db.mysql({
            'host':'localhost',
            'user':'root',
            'passwd':'adminrootkl',
            'db':'qiche',
            'prefix':'kl_',
            'charset':'utf8'
        })
#取brand数据
url='http://www.epicc.com.cn/ecar/car/carModel/getCarModelFromJYDB'
http.setheaders('''\
Host:www.epicc.com.cn
Origin:http://www.epicc.com.cn
Referer:http://www.epicc.com.cn/ecar/proposal/normalProposal
User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36
X-Requested-With:XMLHttpRequest\
''')

#查询品牌#################################################
try:
    for i in range(26):
        code=chr(i+ord('A'))
        tjdata=postdata['brand'].replace('[CODE]',code)
        r=http.posturl(url,tjdata)
        content=''
        if not http.lasterror:
            content=r.read().decode()
            if content:
                try:
                    info=json.loads(content)
                    if info['head']['errorCode']=='91':
                        db.table('0brand').where({'id':i['id']}).save({'status':2})
                    else:
                        brandlist=info['body']['Element']['brandIcons']['FcBrand']
                        for a in brandlist:
                            result=db.table('0brand').where(a).count()
                            if result<=0:
                                db.table('0brand').add(a)
                                print('adding %s'%a)
                except Exception as e:
                    print(e)
        else:
            print(http.lasterror)

except Exception as e:
    print(e)
os.system('pause')