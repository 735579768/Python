import sys,time,msvcrt
sys.path.append('../../lib/')
import kl_db
db=kl_db.mysql({
            'host':'localhost',
            'user':'root',
            'passwd':'adminrootkl',
            'db':'spiders_db',
            'prefix':'kl_',
            'charset':'utf8'
        })
keywords=input('导出区域关键字:')

niming=input('导出匿名等级:')

proxylist=db.table('proxy').where({
	'status':'1',
	'area':['like','%'+keywords+'%'],
    'niming':['like','%'+niming+'%'],
	'response_time':['lt','5']
	}).order('response_time asc').select()
proxylist=proxylist.fetchall()
f=open('proxy.txt','w')
for i in proxylist:
    f.write('%s:%s\n'%(i['ip'],i['port']))
f.close()

input('导出完毕...')
