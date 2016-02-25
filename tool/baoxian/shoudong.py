'''
采集排气量 下面的手动和自动 和配置型号  数据
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
        brandlist=db.table('paiqiliang').where({'status':2}).order('id asc').select()
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
body.jyFlag:40
body.jyType:
body.jyIcon:
body.jyBrandName:
body.jyBrandId:
body.jyFamilyId:
body.jyGroupId:[GROUPID]
body.jyDisplacement:
body.jyGearbox:
body.jyParentId:
body.jyFgwCode:请选择
body.comCode:41010088\
'''
            postdata=postdata.replace('[GROUPID]',i['groupId'])
            r=http.posturl(url,postdata)
            content=''
            if not http.lasterror:
                content=r.read().decode()
                if content:
                    try:
                        info=json.loads(content)
                        if info['head']['errorCode']=='91':
                            db.table('paiqiliang').where({'id':i['id']}).save({'status':2})
                        else:
                            xhlist=info['body']['Element']['parents']['FcParent']
                            addres=True
                            for a in xhlist:
                                result=db.table('shoudong').where(a).count()
                                if result<=0:
                                    res=db.table('shoudong').add(a)
                                    if res<=0:
                                        addres=False
                                print(a)
                    except Exception as e:
                        log.write('add %s  error!'%(i['groupId']))
                        print(e)
            else:
                print(http.lasterror)
            #查询排气量
            postdata='''\
areaCode:41000000
cityCode:41010000
comCode:41010088
jyImportFlag:
head.requestType:01
head.requestCode:
head.checkStr:
head.channelNo:
body.jyFlag:50
body.jyType:
body.jyIcon:
body.jyBrandName:
body.jyBrandId:
body.jyFamilyId:
body.jyGroupId:[GROUPID]
body.jyDisplacement:
body.jyGearbox:1
body.jyParentId:
body.jyFgwCode:请选择
body.comCode:41010088\
'''
            postdata=postdata.replace('[GROUPID]',i['groupId'])
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
                        db.table('paiqiliang').where({'id':i['id']}).save({'status':2})
                        print('%s not result!'%i['groupId'])
                    else:
                        xhlist=info['body']['Element']['parents']['FcParent']
                        addres=True
                        for a in xhlist:
                            result=db.table('peizhixinghao').where(a).count()
                            if result<=0:
                                res=db.table('peizhixinghao').add(a)
                                if res<=0:
                                    addres=False
                            print(a)
                        if addres:
                            db.table('paiqiliang').where({'id':i['id']}).save({'status':1})
                except Exception as e:
                    log.write('add %s  error!'%(i['groupId']))
                    print(e)
    except Exception as e:
        print(e)
os.system('pause')