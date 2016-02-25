import kl_db,os,kl_download
db=kl_db.mysql({
            'host':'localhost',
            'user':'root',
            'passwd':'adminrootkl',
            'db':'mydata',
            'prefix':'kl_',
            'charset':'utf8'
        })
download=kl_download.kl_download()
piclist=db.table('brand').select()
for i in piclist:
    url='http://www.epicc.com.cn/ecar/car/carModel/showPic?path=%s'%i['brandPic']
    outdir="./Uploads/image/20160225"
    filename=os.path.basename(url)
    print('downloading %s'%url)
    pic=download.downimage(url,outdir,filename)
    db.table('brand').where({'id':i['id']}).save({'pic':pic.replace('./','/')})

piclist=db.table('chekuanpic').select()
for i in piclist:
    url='http://www.epicc.com.cn/ecar/car/carModel/showPic?path=%s'%i['thumbnailPath']
    outdir="./Uploads/image/20160225"
    filename=os.path.basename(url)
    print('downloading %s'%url)
    pic=download.downimage(url,outdir,filename)
    db.table('brand').where({'id':i['id']}).save({'pic':pic.replace('./','/')})