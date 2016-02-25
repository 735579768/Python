'''
采集 车款下面的  图片 排气量
'''
import kl_http,kl_db,os,json,kl_log
http=kl_http.kl_http()
log=kl_log.kl_log('brand')
db=kl_db.mysql({
            'host':'localhost',
            'user':'root',
            'passwd':'adminrootkl',
            'db':'mydata',
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
cjbrand=False
cjchexingpinpai=False
cjchekuan=True

#查询车款图片
if cjchekuan:
    try:
        #查询车款
        url='http://www.epicc.com.cn/ecar/car/carModel/getCarModelFromJYDB'
        brandlist=db.table('chekuan').where({'status':0}).order('id asc').select()
        brandlist=brandlist.fetchall()
        for i in brandlist:
            postdata='''\
areaCode:41000000
cityCode:41010000
comCode:41010088
jyImportFlag:
head.requestType:01
head.requestCode:
head.checkStr:
head.channelNo:
body.jyFlag:60
body.jyType:
body.jyIcon:
body.jyBrandName:一汽奥迪A3
body.jyBrandId:
body.jyFamilyId:[FAMILYID]
body.jyGroupId:[GROUPID]
body.jyDisplacement:请选择
body.jyGearbox:
body.jyParentId:
body.jyFgwCode:请选择
body.comCode:41010088\
'''
            postdata=postdata.replace('[GROUPID]',i['groupId'])
            postdata=postdata.replace('[FAMILYID]',i['familyId'])
            r=http.posturl(url,postdata)
            content=''
            if not http.lasterror:
                content=r.read().decode()
                if content:
                    try:
                        info=json.loads(content)
                        if info['head']['errorCode']=='91':
                            db.table('chekuan').where({'id':i['id']}).save({'status':2})
                        else:
                            xhlist=info['body']['Element']['parents']['FcGroup']
                            addres=True
                            for a in xhlist:
                                result=db.table('chekuanpic').where(a).count()
                                if result<=0:
                                    res=db.table('chekuanpic').add(a)
                                    if res<=0:
                                        addres=False
                                print(a)
                    except Exception as e:
                        log.write('add %s %s error!'%(i['groupName'],i['familyId']))
                        print(e)
            else:
                print(http.lasterror)
            #查询排气量
            postdata='''\
areaCode:41000000
cityCode:41010000
comCode:41010088
jyImportFlag:1
head.requestType:01
head.requestCode:
head.uuid:de028895-035c-4908-bc73-e625ff095c21
head.sessionId:de028895-035c-4908-bc73-e625ff095c21
head.checkStr:
head.channelNo:
body.jyFlag:30
body.jyType:
body.jyIcon:
body.jyBrandName:
body.jyBrandId:402880ef0ca9c2b6010cd19acf460187
body.jyFamilyId:[FAMILYID]
body.jyGroupId:[GROUPID]
body.jyDisplacement:请选择
body.jyGearbox:1
body.jyParentId:402880882727cbc701273c2cb90a0caf
body.jyFgwCode:请选择
body.comCode:41010088\
'''
            postdata=postdata.replace('[GROUPID]',i['groupId'])
            postdata=postdata.replace('[FAMILYID]',i['familyId'])
            r=http.posturl(url,postdata)
            content=''
            if not http.lasterror:
                content=r.read().decode()
            else:
                print(http.lasterror)
            if content:
                try:
                    info=json.loads(content)
                    if info['head']['errorCode']=='91':
                        db.table('chekuan').where({'id':i['id']}).save({'status':2})
                    else:
                        xhlist=info['body']['Element']['parents']['FcParent']
                        addres=True
                        for a in xhlist:
                            result=db.table('paiqiliang').where(a).count()
                            if result<=0:
                                res=db.table('paiqiliang').add(a)
                                if res<=0:
                                    addres=False
                            print(a)
                        if addres:
                            db.table('chekuan').where({'id':i['id']}).save({'status':1})
                except Exception as e:
                    log.write('add %s %s error!'%(i['groupName'],i['familyId']))
                    print(e)
    except Exception as e:
        print(e)
os.system('pause')