# -*- coding: utf-8 -*-
import sys,threading,_thread, time,msvcrt,json
sys.path.append('../../lib/')
import kl_http,kl_db, kl_reg,kl_progress
#from queue import Queue
regex=kl_reg
http=kl_http.kl_http()
http.autoUserAgent=True



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
        data=r.read().decode()
        if data.find('#ok#')!=-1:
            jso=json.loads(data)
            proxyfile.write('%s:%s\n'%(i['ip'],i['port']))
            print('代理:%s:%s %s it\'s ok! responsetime: %f  S'%(i['ip'],i['port'],jso['niming'],ht.responsetime))
    curnum-=1
    mylock.release()  #Release the lock.

maxnum=30
curnum=0
progress.settext('正在测试代理')
progress.show()
threads=[]
f=open('proxy.txt','r')
s=f.read()
f.close()
proxylist=s.splitlines()

proxyfile=open('proxy.txt','w')
for i in proxylist:
    i=i.split(':')
    i={'ip':i[0],'port':i[1]}
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

proxyfile.close()
progress.stop()
time.sleep(2)
input('测试完毕...')
