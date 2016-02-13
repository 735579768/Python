import sys,threading, time
sys.path.append('../../lib/')
import kl_http,kl_db, kl_reg
#from queue import Queue
regex=kl_reg
http=kl_http.kl_http()
http.autoUserAgent=True

def filterhtml(s):
    s=regex.replace(r'<.*?>','',s, regex.I|regex.S)
    s=regex.replace(r'\s+','',s, regex.I|regex.S)
    return s

db=kl_db.mysql({
            'host':'localhost',
            'user':'root',
            'passwd':'adminrootkl',
            'db':'mydata',
            'prefix':'kl_',
            'charset':'utf8'
        })
#代理采集地址
proxy=[
    #360免费代理
    {
    'proxyurl':'http://www.proxy360.cn/Region/China',
    'proxyitem':'proxylistitem.*?<span.*?>(?P<ip>.*?)</span>.*?<span.*?>(?P<port>.*?)</span>.*?<span.*?>(?P<proxy_type>.*?)</span>.*?<span.*?>(?P<proxy_area>.*?)</span>.*?ratingStar'
    },
    #西刺免费代理IP
    {
    'proxyurl':'http://www.xicidaili.com/nn/',
    'proxyitem':'<td>(?P<ip>\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3})</td>.*?<td>(?P<port>\d{1,5})</td>.*?<td>(?P<proxy_area>.*?)</td>.*?<td>(?P<proxy_type>.*?)</td>'
    },
    {
    'proxyurl':'http://www.xicidaili.com/nt/',
    'proxyitem':'<td>(?P<ip>\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3})</td>.*?<td>(?P<port>\d{1,5})</td>.*?<td>(?P<proxy_area>.*?)</td>.*?<td>(?P<proxy_type>.*?)</td>'
    },
    #快代理
    {
    'proxyurl':'http://www.kuaidaili.com/proxylist/1/',
    'proxyitem':'<td>(?P<ip>\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3})</td>.*?<td>(?P<port>\d{1,5})</td>.*?<td>(?P<proxy_type>.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(?P<proxy_area>.*?)</td>'
    },
    {
    'proxyurl':'http://www.kuaidaili.com/proxylist/2/',
    'proxyitem':'<td>(?P<ip>\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3})</td>.*?<td>(?P<port>\d{1,5})</td>.*?<td>(?P<proxy_type>.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(?P<proxy_area>.*?)</td>'
    },
    {
    'proxyurl':'http://www.kuaidaili.com/proxylist/3/',
    'proxyitem':'<td>(?P<ip>\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3})</td>.*?<td>(?P<port>\d{1,5})</td>.*?<td>(?P<proxy_type>.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(?P<proxy_area>.*?)</td>'
    },
    {
    'proxyurl':'http://www.kuaidaili.com/proxylist/4/',
    'proxyitem':'<td>(?P<ip>\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3})</td>.*?<td>(?P<port>\d{1,5})</td>.*?<td>(?P<proxy_type>.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(?P<proxy_area>.*?)</td>'
    },
    {
    'proxyurl':'http://www.kuaidaili.com/proxylist/5/',
    'proxyitem':'<td>(?P<ip>\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3})</td>.*?<td>(?P<port>\d{1,5})</td>.*?<td>(?P<proxy_type>.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(?P<proxy_area>.*?)</td>'
    }
]
for i in proxy:
    print('正在采集: %s'%i['proxyurl'])
    r=http.geturl(i['proxyurl'])
    if not r:
        print('[%s ERROR CODE]:%s'%(i['proxyurl'], http.lasterror.code))
        print(http.lasterror)
        continue
    con=r.read().decode()

    proxyitem=regex.finditer(i['proxyitem'], con, regex.I|regex.S)
    for a in proxyitem:
        ip1=a.group('ip')
        port1=a.group('port')
        proxy_type1=a.group('proxy_type')
        proxy_area1=a.group('proxy_area')
        ma={
            'ip':filterhtml(ip1),
            'port':filterhtml(port1),
            'proxy_type':filterhtml(proxy_type1),
            'proxy_area':filterhtml(proxy_area1)
            }
        result=db.table('proxy').where(ma).count()
        if result<=0:
            print('添加新代理:%s:%s %s %s'%(ma['ip'],ma['port'],ma['proxy_type'],ma['proxy_area']))
            db.table('proxy').add(ma)


#测试代理是否可用
print('测试代理是否可用...')
#测试线程函数
maxnum=30
curnum=0
def testProxy(i):
    global curnum
    curnum+=1
    print('正在测试代理:%s:%s %s %s'%(i['ip'],i['port'],i['proxy_type'],i['proxy_area']))
    ht=kl_http.kl_http()
    ht.setproxy('','','%s:%s'%(i['ip'],i['port']))
    r=ht.geturl('http://1212.ip138.com/ic.asp')
    if r!=None:
        data=filterhtml(r.read().decode('gb2312'))
        print(data)
        if data.find('您的IP地址')!=-1:
            db.table('proxy').where({'id':i['id']}).save({'status':'1','update_time':int(time.time())})
            print('代理:%s:%s %s %s it is ok!'%(i['ip'],i['port'],i['proxy_type'],i['proxy_area']))
    else:
        db.table('proxy').where({'id':i['id']}).save({'status':'0','update_time':int(time.time())})
        print('代理:%s:%s %s %s it is not ok!'%(i['ip'],i['port'],i['proxy_type'],i['proxy_area']))
    curnum=curnum-1

proxylist=db.table('proxy').order('id asc').select()
proxylist=proxylist.fetchall()

threads=[]
for i in proxylist:
    t=threading.Thread(target=testProxy,args=(i,))
    threads.append(t)


while len(threads)>0:
    #print('当前线程数:%s \r'%curnum)
    if curnum<maxnum:
        threads.pop().start()
    #time.sleep(1)

while curnum>0:
    time.sleep(1)


input('测试完毕...')
