'''
采集 车款的图片和排气量
'''
import kl_http,kl_db,os,json,kl_log
from postdata import postdata
addnum=0
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
http.autoUserAgent=True
http.setheaders('''\
Host:www.epicc.com.cn
Origin:http://www.epicc.com.cn
Referer:http://www.epicc.com.cn/ecar/proposal/normalProposal
User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36
X-Requested-With:XMLHttpRequestContent-Type: application/x-www-form-urlencoded\
''')

#查询车款图片
try:
    url='http://www.epicc.com.cn/ecar/car/carModel/getCarModelFromJYDB'
    # model={
    #  '2chekuan':{'_as':'a','field':'*'},
    #  '1chexingpinpai':{'_as':'b','field':'brandId','_on':'a.familyId=b.familyId'}
    # }
    # brandlist=db.join(model).where({'a.status':0}).getarr()
    brandlist=db.table('2chekuan').where({'status':0}).order('id asc').getarr()
    for i in brandlist:
        tjdata=postdata['chekuanpic'].replace('[GROUPID]',i['groupId'])
        r=http.posturl(url,tjdata)
        content=''
        if not http.lasterror:
            content=r.read().decode()
            if content:
                try:
                    info=json.loads(content)
                    if info['head']['errorCode']=='91':
                        db.table('2chekuan').where({'id':i['id']}).save({'status':2})
                    else:
                        xhlist=info['body']['Element']['parents']['FcGroup']
                        addres=True
                        for a in xhlist:
                            result=db.table('chekuanpic').where(a).count()
                            if result<=0:
                                res=db.table('chekuanpic').add(a)
                                if res<=0:
                                    addres=False
                                else:
                                    print('adding %s'%a)
                        # if addres:
                        #     db.table('2chekuan').where({'id':i['id']}).save({'status':1})
                except Exception as e:
                    log.write('add %s %s error!'%(i['groupName'],i['familyId']))
                    print(e)
        else:
            print(http.lasterror)
#查询排气量
        tjdata=postdata['paiqiliang'].replace('[GROUPID]',i['groupId'])
        r=http.posturl(url,tjdata)
        content=''
        if not http.lasterror:
            content=r.read().decode()
        else:
            print(http.lasterror)
        if content:
            try:
                info=json.loads(content)
                if info['head']['errorCode']=='91':
                    db.table('2chekuan').where({'id':i['id']}).save({'status':2})
                else:
                    xhlist=info['body']['Element']['parents']['FcParent']
                    addres=True
                    for a in xhlist:
                        a['brandId']=i['brandId']
                        a['familyId']=i['familyId']
                        a['groupId']=i['groupId']
                        result=db.table('3paiqiliang').where(a).count()
                        if result<=0:
                            res=db.table('3paiqiliang').add(a)
                            if res<=0:
                                addres=False
                            else:
                                print('adding %s'%a)
                                addnum+=1
                        else:
                            print('it is exist! %s'%a)
                    if addres:
                        db.table('2chekuan').where({'id':i['id']}).save({'status':1})
            except Exception as e:
                log.write('add %s %s error!'%(i['groupName'],i['familyId']))
                print(e)
except Exception as e:
    print(e)


print('already add %d'%addnum)
os.system('pause')