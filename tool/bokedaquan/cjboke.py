import sys,random
sys.path.append('../../lib/')
import kl_http,kl_db, kl_reg
regex=kl_reg
http=kl_http.kl_http()
http.autoUserAgent=True

#读取代理文件
dlf=open('proxy.txt','r')
proxyip=dlf.read()
dlf.close()
proxyip=proxyip.split('\n')


def getmovieinfo(s):
    re_title='<h1>.*?<span.*?>(.*?)</span>.*?</h1>'
    re_content='<div class\=\"article\">.*?<div class\=\"aside\">'
    re_daoyan='导演</span>:(.*?)<br/>'
    re_zhuyan='主演</span>:(.*?)<br/>'
    re_shangying='首播:|上映日期:(.*?)<br/>'
    re_leixing='类型:(.*?)<br/>'
    re_youming='又名:(.*?)<br/>'
    re_pianchang='片长:(.*?)<br/>'
    re_pingfen='豆瓣评分.*?<strong.*?>(.*?)</strong>'
    ma=regex.findall(re_content,s, regex.L|regex.S)
    con={
        'title':filterhtml(re_title,s),
        'daoyan':filterhtml(re_daoyan,ma[0]),
        'zhuyan':filterhtml(re_zhuyan,ma[0]),
        'shangying':filterhtml(re_shangying,ma[0]),
        'leixing':filterhtml(re_leixing,ma[0]),
        'youming':filterhtml(re_youming,ma[0]),
        'pianchang':filterhtml(re_pianchang,ma[0]),
        'pingfen':filterhtml(re_pingfen,ma[0])
    }
    return con
def filterhtml(pattern,string):
    m=regex.findall(pattern,string,regex.I|regex.S)
    if len(m)>0:
        s=regex.replace(r'<.*?>','',m[0], regex.I|regex.S)
        s=regex.replace(r'\s{2,}',' ',s, regex.I|regex.S)
        return s
    else:
        return ''

db=kl_db.mysql({
            'host':'localhost',
            'user':'root',
            'passwd':'adminrootkl',
            'db':'douban',
            'prefix':'kl_',
            'charset':'utf8'
        })

databool=True

proxyiplen=len(proxyip)

while databool:
    mlist=db.table('url').where({
        'status':[['eq','2'],['eq','503'],['eq','500'],['eq','403'],['eq','504'],'or']
        }).limit(10).order('id asc').select()
    mlist=mlist.fetchall()
    if not (len(mlist)>0):
        databool=False
        break
    try:
        for i in mlist:
            print(i['url'])
            proxip=proxyip[random.randint(0,proxyiplen-1)]
            http.setproxy('','',proxip)
            r=http.geturl(i['url'])
            if not r:
                res=db.table('url').where("id=%s"%i['id']).save({'status':http.lasterror.code})
                print('%s 数据采集异常...'%i['url'])

                continue
            rr=r.read().decode()
            data=getmovieinfo(rr)
            data['leixing']=data['leixing'].replace(' ','')
            data['url_id']=i['id']
            result=db.table('movies').add(data)
            if result>0:
                res=db.table('url').where("id=%s"%i['id']).save({'status':1})
                if res==0:
                    print('更新数据采集失败...%s'%i['url'])
            http.resetsession()
    except:
        print('%s 数据采集异常...'%i['url'])

input('输入任意键继续...')
