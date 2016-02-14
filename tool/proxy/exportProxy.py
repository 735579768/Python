import sys
sys.path.append('../../lib/')
import kl_db

db=kl_db.mysql({
            'host':'localhost',
            'user':'root',
            'passwd':'adminrootkl',
            'db':'mydata',
            'prefix':'kl_',
            'charset':'utf8'
        })

proxylist=db.table('proxy').where({'status':'1','response_time':['lt','1']}).order('response_time asc').select()
proxylist=proxylist.fetchall()
f=open('export.txt','w')
for i in proxylist:
    f.write('%s:%s\n'%(i['ip'],i['port']))
f.close()

input('导出完毕...')
