# -*- coding: utf-8 -*-
import sys,threading,_thread, time,msvcrt,json
sys.path.append('../../lib/')
import kl_http,kl_db, kl_reg,kl_progress
#from queue import Queue
regex=kl_reg
http=kl_http.kl_http()
http.autoUserAgent=True
def readInput(caption, default, timeout=10):
    start_time = time.time()
    sys.stdout.write('%s(%d秒自动跳过):' % (caption,timeout))
    sys.stdout.flush()
    input = ''

    while True:
        ini=msvcrt.kbhit()
        try:
            if ini:
                chr = msvcrt.getche()
                if ord(chr) == 13:  # enter_key
                    break
                elif ord(chr) >= 32:
                    input += chr.decode()
        except Exception as e:
            pass
        if len(input) == 0 and time.time() - start_time > timeout:
            break
    print ('')  # needed to move to next line
    if len(input) > 0:
        return input+''
    else:
        return default

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
    'proxyitem':'proxylistitem.*?<span.*?>(?P<ip>.*?)</span>.*?<span.*?>(?P<port>.*?)</span>.*?<span.*?>(?P<niming>.*?)</span>.*?<span.*?>(?P<proxy_area>.*?)</span>.*?ratingStar',
    'charset':'utf-8',
    'area':'中国'
    },
    #西刺免费代理IP
    {
    'proxyurl':'http://www.xicidaili.com/nn/1',
    'proxyitem':'<td>(?P<ip>\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3})</td>.*?<td>(?P<port>\d{1,5})</td>.*?<td>(?P<proxy_area>.*?)</td>.*?<td>(?P<niming>.*?)</td>.*?<td>(?P<proxy_type>.*?)</td>',
    'charset':'utf-8',
    'area':'中国'
    },
    {
    'proxyurl':'http://www.xicidaili.com/nn/2',
    'proxyitem':'<td>(?P<ip>\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3})</td>.*?<td>(?P<port>\d{1,5})</td>.*?<td>(?P<proxy_area>.*?)</td>.*?<td>(?P<niming>.*?)</td>.*?<td>(?P<proxy_type>.*?)</td>',
    'charset':'utf-8',
    'area':'中国'
    },
    {
    'proxyurl':'http://www.xicidaili.com/nn/3',
    'proxyitem':'<td>(?P<ip>\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3})</td>.*?<td>(?P<port>\d{1,5})</td>.*?<td>(?P<proxy_area>.*?)</td>.*?<td>(?P<niming>.*?)</td>.*?<td>(?P<proxy_type>.*?)</td>',
    'charset':'utf-8',
    'area':'中国'
    },
    {
    'proxyurl':'http://www.xicidaili.com/nn/4',
    'proxyitem':'<td>(?P<ip>\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3})</td>.*?<td>(?P<port>\d{1,5})</td>.*?<td>(?P<proxy_area>.*?)</td>.*?<td>(?P<niming>.*?)</td>.*?<td>(?P<proxy_type>.*?)</td>',
    'charset':'utf-8',
    'area':'中国'
    },
    #快代理
    {
    'proxyurl':'http://www.kuaidaili.com/proxylist/1/',
    'proxyitem':'<td>(?P<ip>\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3})</td>.*?<td>(?P<port>\d{1,5})</td>.*?<td>(?P<niming>.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(?P<proxy_area>.*?)</td>',
    'charset':'utf-8',
    'area':'中国'
    },
    {
    'proxyurl':'http://www.kuaidaili.com/proxylist/2/',
    'proxyitem':'<td>(?P<ip>\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3})</td>.*?<td>(?P<port>\d{1,5})</td>.*?<td>(?P<niming>.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(?P<proxy_area>.*?)</td>',
    'charset':'utf-8',
    'area':'中国'
    },
    {
    'proxyurl':'http://www.kuaidaili.com/proxylist/3/',
    'proxyitem':'<td>(?P<ip>\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3})</td>.*?<td>(?P<port>\d{1,5})</td>.*?<td>(?P<niming>.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(?P<proxy_area>.*?)</td>',
    'charset':'utf-8',
    'area':'中国'
    },
    {
    'proxyurl':'http://www.kuaidaili.com/proxylist/4/',
    'proxyitem':'<td>(?P<ip>\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3})</td>.*?<td>(?P<port>\d{1,5})</td>.*?<td>(?P<niming>.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(?P<proxy_area>.*?)</td>',
    'charset':'utf-8',
    'area':'中国'
    },
    {
    'proxyurl':'http://www.kuaidaili.com/proxylist/5/',
    'proxyitem':'<td>(?P<ip>\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3})</td>.*?<td>(?P<port>\d{1,5})</td>.*?<td>(?P<niming>.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(?P<proxy_area>.*?)</td>',
    'charset':'utf-8',
    'area':'中国'
    },
    #免费代理 - 米扑代理
    {
    'proxyurl':'http://proxy.mimvp.com/free.php?proxy=in_hp',
    'proxyitem':'',
    'charset':'utf-8',
    'area':'中国'
    },




    #IPCN 国家地区免费代理
    {
    'proxyurl':'http://proxy.ipcn.org/country/?s=cn',
    'proxyitem':'<td>.*?(?P<ip>\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3}):(?P<port>\d{1,5}).*?(?P<niming>.*?)(?P<proxy_area>.*?)</td>',
    'charset':'gb2312',
    'area':'中国'
    },
    {
    'proxyurl':'http://proxy.ipcn.org/country/?q=US',
    'proxyitem':'<td>.*?(?P<ip>\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3}):(?P<port>\d{1,5}).*?(?P<niming>.*?)(?P<proxy_area>.*?)</td>',
    'charset':'gb2312',
    'area':'美国'
    },
    {
    'proxyurl':'http://proxy.ipcn.org/country/?q=VI',
    'proxyitem':'<td>.*?(?P<ip>\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3}):(?P<port>\d{1,5}).*?(?P<niming>.*?)(?P<proxy_area>.*?)</td>',
    'charset':'gb2312',
    'area':'美国的'
    },
    {
    'proxyurl':'http://proxy.ipcn.org/country/?q=VG',
    'proxyitem':'<td>.*?(?P<ip>\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3}):(?P<port>\d{1,5}).*?(?P<niming>.*?)(?P<proxy_area>.*?)</td>',
    'charset':'gb2312',
    'area':'英国'
    }
]

iscaiji=readInput('是否采集代理(y/n)','n')
iscaiji=iscaiji.lower()


if iscaiji=='y':
    istable=readInput('是否重新创建数据表(y/n)','n')

    istable=istable.lower()
    if istable=='y':
        db.query('''\
            DROP TABLE IF EXISTS `kl_proxy`;
            CREATE TABLE `kl_proxy` (
              `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
              `ip` varchar(255) DEFAULT NULL,
              `port` varchar(255) DEFAULT NULL,
              `proxy_type` varchar(255) DEFAULT NULL,
              `niming` varchar(255) DEFAULT NULL,
              `proxy_area` varchar(255) DEFAULT NULL,
              `status` tinyint(1) DEFAULT '0',
              `response_time` float(11,5) DEFAULT NULL,
              `proxy_ip` varchar(255) DEFAULT NULL,
              `zhenshi_ip` varchar(255) DEFAULT NULL,
              `update_time` int(11) DEFAULT NULL,
              `area` varchar(255) DEFAULT NULL,
              PRIMARY KEY (`id`)
            ) ENGINE=MyISAM AUTO_INCREMENT=879 DEFAULT CHARSET=utf8;\
            ''')
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
            niming1=a.group('niming')
            proxy_type1='http'
            if 'proxy_type' in a.groupdict():
                proxy_type1=a.group('proxy_type')
            proxy_type=proxy_type.lower()

            proxy_area1=a.group('proxy_area')
            ma={
                'ip':filterhtml(ip1),
                'port':filterhtml(port1),
                'niming':filterhtml(niming1),
                'proxy_type':filterhtml(proxy_type1),
                'proxy_area':filterhtml(proxy_area1),
                'update_time':time.time(),
                'area':i['area']
                }
            result=db.table('proxy').where(ma).count()
            if result<=0:
                print('添加新代理:%s:%s %s %s'%(ma['ip'],ma['port'],ma['niming'],ma['proxy_type']))
                db.table('proxy').add(ma)



progress=kl_progress.kl_progress('')
progress.start()
progress.hide()
#测试代理是否可用
mylock = _thread.allocate_lock()  #线程锁
#测试线程函数
def testProxy(i):
    global curnum
    #print('正在测试代理:%s:%s %s %s'%(i['ip'],i['port'],i['proxy_type'],i['proxy_area']))
    # sys.stdout.write('正在测试代理:%s:%s ...'%(i['ip'],i['port'])+"\r")
    # sys.stdout.flush()
    progress.settext('正在测试代理:%s:%s'%(i['ip'],i['port']))
    ht=kl_http.kl_http()
    ht.setproxy('','','%s:%s'%(i['ip'],i['port']))
    r=ht.geturl('http://proxy.59vip.cn')
    mylock.acquire() #Get the lock
    if r!=None:
        data=filterhtml(r.read().decode())
        if data.find('#ok#')!=-1:
            jso=json.loads(data)
            db.table('proxy').where({'id':i['id']}).save({
                'status':'1',
                'response_time':ht.responsetime,
                'niming':jso['niming'],
                'proxy_ip':jso['proxy_ip'],
                'zhenshi_ip':jso['ip'],
                'update_time':int(time.time())
                })
            print('代理:%s:%s %s it\'s ok! responsetime: %f  S'%(i['ip'],i['port'],i['proxy_type'],ht.responsetime))
    else:
        #db.table('proxy').where({'id':i['id']}).save({'status':'0','update_time':int(time.time())})
        db.table('proxy').where({'id':i['id']}).delete()
        #print('代理:%s:%s %s %s it is not ok!'%(i['ip'],i['port'],i['proxy_type'],i['proxy_area']))
    curnum-=1
    mylock.release()  #Release the lock.


istest=readInput('是否测试数据库的代理是否可用(y/n)','n')
if istest=='':
    istest='n'
istest=istest.lower()




maxnum=30
curnum=0
if istest=='yes':
    input('按任意键开始测试代理是否可用...')
    progress.settext('正在测试代理')
    progress.show()
    db.table('proxy').where({'status':'1'}).save({'status':0})
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

    progress.settext('马上测试完毕,请稍等')
    time.sleep(2)
    while True:
        if curnum==0:
            break
        time.sleep(1)

    db.table('proxy').where({'status':'0'}).delete()
    progress.stop()
    time.sleep(2)
    input('测试完毕...')
else:
    progress.stop()
    time.sleep(2)
    input('按任意键结束...')
