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
cjbrand=False
cjchexingpinpai=False
cjchekuan=True
cjpaiqiliang=False
cjsdzd=False
#取brand数据
url='http://www.epicc.com.cn/ecar/car/carModel/getCarModelFromJYDB'
http.setheaders('''\
Host:www.epicc.com.cn
Origin:http://www.epicc.com.cn
Referer:http://www.epicc.com.cn/ecar/proposal/normalProposal
User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36
X-Requested-With:XMLHttpRequest\
''')

#查询品牌#################################################
if cjbrand:
    try:
        for i in range(26):
            code=chr(i+ord('A'))
            postdata='''\
areaCode:41000000
cityCode:41010000
comCode:41010088
jyImportFlag:
head.requestType:01
head.requestCode:
head.checkStr:
head.channelNo:
body.jyFlag:11
body.jyType:
body.jyIcon:[CODE]
body.jyBrandName:
body.jyBrandId:
body.jyFamilyId:
body.jyGroupId:
body.jyDisplacement:请选择
body.jyGearbox:
body.jyParentId:
body.jyFgwCode:请选择
body.comCode:41010088\
     '''
            postdata=postdata.replace('[CODE]',code)
            r=http.posturl(url,postdata)
            content=''
            if not http.lasterror:
                content=r.read().decode()
                if content:
                    try:
                        info=json.loads(content)
                        brandlist=info['body']['Element']['brandIcons']['FcBrand']
                        for a in brandlist:
                            result=db.table('brand').where(a).count()
                            if result<=0:
                                db.table('brand').add(a)
                            print(a)
                    except Exception as e:
                        print(e)
            else:
                print(http.lasterror)

    except Exception as e:
        print(e)

#查询车型品牌#################################################
if cjchexingpinpai:
    try:
        url='http://www.epicc.com.cn/ecar/car/carModel/getCarModelFromJYDB'
        brandlist=db.table('brand').where({'status':0}).select()
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
body.jyFlag:20
body.jyType:
body.jyIcon:H
body.jyBrandName:[BRANDNAME]
body.jyBrandId:[BRANDID]
body.jyFamilyId:I0000000000000000210000000000725
body.jyGroupId:4028b28839aa3b5e0139b35baf700d41
body.jyDisplacement:请选择
body.jyGearbox:
body.jyParentId:
body.jyFgwCode:请选择
body.comCode:41010088\
'''
            postdata=postdata.replace('[BRANDNAME]',i['brandName'])
            postdata=postdata.replace('[BRANDID]',i['brandId'])
            r=http.posturl(url,postdata)
            content=''
            if not http.lasterror:
                content=r.read().decode()
                if content:
                    try:
                        info=json.loads(content)
                        xhlist=info['body']['Element']['familys']['FcFamily']
                        addres=True
                        for a in xhlist:
                            result=db.table('chexingpinpai').where(a).count()
                            if result<=0:
                                res=db.table('chexingpinpai').add(a)
                                if res<=0:
                                    addres=False
                            print(a)
                        if addres:
                            db.table('brand').where({'id':i['id']}).save({'status':1})
                    except Exception as e:
                        print(e)
            else:
                print(http.lasterror)
    except Exception as e:
        print(e)

#查询车款
if cjchekuan:
    try:
        #查询车款
        url='http://www.epicc.com.cn/ecar/car/carModel/getCarModelFromJYDB'
        brandlist=db.table('chexingpinpai').where({'status':0}).order('id asc').select()
        brandlist=brandlist.fetchall()
        for i in brandlist:
            postdata='''\
areaCode:41000000
cityCode:41010000
comCode:41010088
jyImportFlag:0
head.requestType:01
head.requestCode:
head.checkStr:
head.channelNo:
body.jyFlag:21
body.jyType:
body.jyIcon:A
body.jyBrandName:[BRANDNAME]
body.jyBrandId:
body.jyFamilyId:[FAMILYID]
body.jyGroupId:
body.jyDisplacement:请选择
body.jyGearbox:
body.jyParentId:
body.jyFgwCode:请选择
body.comCode:41010088\
'''
            postdata=postdata.replace('[BRANDNAME]',i['brandName']+i['familyAbbr'])
            postdata=postdata.replace('[FAMILYID]',i['familyId'])
            r=http.posturl(url,postdata)
            content=''
            if not http.lasterror:
                content=r.read().decode()
                if content:
                    try:
                        info=json.loads(content)
                        if info['head']['errorCode']=='91':
                            db.table('chexingpinpai').where({'id':i['id']}).save({'status':2})
                        else:
                            xhlist=info['body']['Element']['groups']['FcGroup']
                            addres=True
                            for a in xhlist:
                                result=db.table('chekuan').where(a).count()
                                if result<=0:
                                    res=db.table('chekuan').add(a)
                                    if res<=0:
                                        addres=False
                                print(a)
                            if addres:
                                db.table('chexingpinpai').where({'id':i['id']}).save({'status':1})
                    except Exception as e:
                        log.write('add %s %s %s error!'%(i['brandName'],i['familyAbbr'],i['familyId']))
                        print(e)
            else:
                print(http.lasterror)
    except Exception as e:
        print(e)
os.system('pause')