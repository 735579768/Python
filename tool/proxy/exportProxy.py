import sys,time,msvcrt
sys.path.append('../../lib/')
import kl_db
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
db=kl_db.mysql({
            'host':'localhost',
            'user':'root',
            'passwd':'adminrootkl',
            'db':'mydata',
            'prefix':'kl_',
            'charset':'utf8'
        })
keywords=readInput('导出区域关键字','中国')

proxylist=db.table('proxy').where({
	'status':'1',
	'area':['like','%'+keywords+'%'],
	'response_time':['lt','1']
	}).order('response_time asc').select()
proxylist=proxylist.fetchall()
f=open('export.txt','w')
for i in proxylist:
    f.write('%s:%s\n'%(i['ip'],i['port']))
f.close()

input('导出完毕...')
