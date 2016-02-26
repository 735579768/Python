import kl_db,os,kl_download
db=kl_db.mysql({
            'host':'localhost',
            'user':'root',
            'passwd':'adminrootkl',
            'db':'qiche',
            'prefix':'kl_',
            'charset':'utf8'
        })
download=kl_download.kl_download()
piclist=db.table('brand').where({'downpic':0}).order('id asc').getarr()
if piclist:
    for i in piclist:
        url='http://www.epicc.com.cn/ecar/car/carModel/showPic?path=%s'%i['brandPic']
        outdir="./Uploads/image/qichebrand"
        filename=os.path.basename(url)
        print('downloading %s'%url)
        pic=download.downimage(url,outdir,filename)
        if pic:
            db.table('brand').where({'id':i['id']}).save({'pic':pic.replace('./','/'),'downpic':1})

piclist=db.table('chekuanpic').where({'downpic':0}).order('id asc').getarr()
if piclist:
    for i in piclist:
        url='http://www.epicc.com.cn/ecar/car/carModel/showPic?path=%s'%i['thumbnailPath']
        outdir="./Uploads/image/qicheks"
        filename=os.path.basename(url)
        print('downloading %s'%url)
        pic=download.downimage(url,outdir,filename)
        if pic:
            db.table('chekuanpic').where({'id':i['id']}).save({'pic':pic.replace('./','/'),'downpic':1})


os.system('pause')