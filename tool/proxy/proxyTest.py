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
db.query('''\
DROP TABLE IF EXISTS `kl_proxy`;
CREATE TABLE `kl_proxy` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `ip` varchar(255) DEFAULT NULL,
  `port` varchar(255) DEFAULT NULL,
  `proxy_type` varchar(255) DEFAULT NULL,
  `proxy_area` varchar(255) DEFAULT NULL,
  `status` tinyint(1) DEFAULT '0',
  `response_time` float(11,5) DEFAULT NULL,
  `update_time` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=879 DEFAULT CHARSET=utf8;\
    ''')
#代理采集地址
proxy=[
    #360免费代理
    {
    'proxyurl':'http://www.proxy360.cn/Region/China',
    'proxyitem':'proxylistitem.*?<span.*?>(?P<ip>.*?)</span>.*?<span.*?>(?P<port>.*?)</span>.*?<span.*?>(?P<proxy_type>.*?)</span>.*?<span.*?>(?P<proxy_area>.*?)</span>.*?ratingStar',
    'charset':'utf-8'
    },
    #西刺免费代理IP
    {
    'proxyurl':'http://www.xicidaili.com/nn/',
    'proxyitem':'<td>(?P<ip>\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3})</td>.*?<td>(?P<port>\d{1,5})</td>.*?<td>(?P<proxy_area>.*?)</td>.*?<td>(?P<proxy_type>.*?)</td>',
    'charset':'utf-8'
    },
    {
    'proxyurl':'http://www.xicidaili.com/nt/',
    'proxyitem':'<td>(?P<ip>\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3})</td>.*?<td>(?P<port>\d{1,5})</td>.*?<td>(?P<proxy_area>.*?)</td>.*?<td>(?P<proxy_type>.*?)</td>',
    'charset':'utf-8'
    },
    #快代理
    {
    'proxyurl':'http://www.kuaidaili.com/proxylist/1/',
    'proxyitem':'<td>(?P<ip>\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3})</td>.*?<td>(?P<port>\d{1,5})</td>.*?<td>(?P<proxy_type>.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(?P<proxy_area>.*?)</td>',
    'charset':'utf-8'
    },
    {
    'proxyurl':'http://www.kuaidaili.com/proxylist/2/',
    'proxyitem':'<td>(?P<ip>\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3})</td>.*?<td>(?P<port>\d{1,5})</td>.*?<td>(?P<proxy_type>.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(?P<proxy_area>.*?)</td>',
    'charset':'utf-8'
    },
    {
    'proxyurl':'http://www.kuaidaili.com/proxylist/3/',
    'proxyitem':'<td>(?P<ip>\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3})</td>.*?<td>(?P<port>\d{1,5})</td>.*?<td>(?P<proxy_type>.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(?P<proxy_area>.*?)</td>',
    'charset':'utf-8'
    },
    {
    'proxyurl':'http://www.kuaidaili.com/proxylist/4/',
    'proxyitem':'<td>(?P<ip>\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3})</td>.*?<td>(?P<port>\d{1,5})</td>.*?<td>(?P<proxy_type>.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(?P<proxy_area>.*?)</td>',
    'charset':'utf-8'
    },
    {
    'proxyurl':'http://www.kuaidaili.com/proxylist/5/',
    'proxyitem':'<td>(?P<ip>\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3})</td>.*?<td>(?P<port>\d{1,5})</td>.*?<td>(?P<proxy_type>.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(?P<proxy_area>.*?)</td>',
    'charset':'utf-8'
    },
    #IPCN 国家地区免费代理
    {
    'proxyurl':'http://proxy.ipcn.org/country/',
    'proxyitem':'<td>.*?(?P<ip>\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3}):(?P<port>\d{1,5}).*?(?P<proxy_type>.*?)(?P<proxy_area>.*?)</td>',
    'charset':'gb2312'
    }
]
for i in proxy:
    print('正在采集: %s'%i['proxyurl'])
    r=http.geturl(i['proxyurl'])
    if not r:
        print('[%s ERROR CODE]:%s'%(i['proxyurl'], http.lasterror.code))
        print(http.lasterror)
        continue
    con=r.read().decode(i['charset'])

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
            'proxy_area':filterhtml(proxy_area1),
            'update_time':time.time()
            }
        result=db.table('proxy').where(ma).count()
        if result<=0:
            print('添加新代理:%s:%s %s %s'%(ma['ip'],ma['port'],ma['proxy_type'],ma['proxy_area']))
            db.table('proxy').add(ma)

input('按任意键开始测试代理是否可用...')

#测试代理是否可用
print('正在测试可用的代理...')
#测试线程函数
def testProxy(i):
    global curnum
    #print('正在测试代理:%s:%s %s %s'%(i['ip'],i['port'],i['proxy_type'],i['proxy_area']))
    sys.stdout.write('正在测试代理:%s:%s ...'%(i['ip'],i['port'])+"\r")
    sys.stdout.flush()
    ht=kl_http.kl_http()
    ht.setproxy('','','%s:%s'%(i['ip'],i['port']))
    r=ht.geturl('http://proxy.59vip.cn')
    if r!=None:
        data=filterhtml(r.read().decode())
        #print(data)
        if data.find('ok')!=-1:
            db.table('proxy').where({'id':i['id']}).save({'status':'1','response_time':ht.responsetime,'update_time':int(time.time())})
            print('代理:%s:%s %s it\'s ok! responsetime: %f  S'%(i['ip'],i['port'],i['proxy_type'],ht.responsetime))
    else:
        #db.table('proxy').where({'id':i['id']}).save({'status':'0','update_time':int(time.time())})
        db.table('proxy').where({'id':i['id']}).delete()
        #print('代理:%s:%s %s %s it is not ok!'%(i['ip'],i['port'],i['proxy_type'],i['proxy_area']))
    curnum-=1
maxnum=30
curnum=0
proxylist=db.table('proxy').where({'status':'0'}).order('id asc').select()
proxylist=proxylist.fetchall()
threads=[]
for i in proxylist:
    while True:
        if curnum<=maxnum:
            t=threading.Thread(target=testProxy,args=(i,))
            t.start()
            curnum+=1
            break
    time.sleep(0.1)


while True:
    if curnum==0:
        break
    sys.stdout.write('马上测试完毕,请稍等...')
    sys.stdout.flush()
    time.sleep(1)

db.table('proxy').where({'status':'0'}).delete()

input('测试完毕...')
