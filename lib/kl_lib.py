import os,tempfile,time,subprocess
from urllib.parse import urlparse
#格式化网页资源请求的路径
def formatUrl(self,requestpath,curpath):
    #请求的url目录
    urldir=os.path.dirname(requestpath)
    url=urlparse(requestpath)
    protocol=url[0]
    hostname=url[1]
    if curpath[0:1]=='/':
        return '%s://%s%s'%(protocol,hostname,curpath)
    else:
        return urldir+'/'+curpath

#创建目录
def createDir(dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

#ocr识别,需要系统中安装tesseract-ocr并将路径添加到系统路径中
def ocr(imgpath,lang=''):
    temp=tempfile.NamedTemporaryFile()
    temppath=temp.name
    temp.close()
    try:
        if lang:
            lang=' -l %s'%lang
        command='tesseract %s %s %s'%(imgpath,temppath,lang)
        resu=subprocess.call(command, shell=True)
        if not  resu:
            filepath=temppath+'.txt'
            f=open(filepath,'r')
            restr=f.read().replace('\n','')
            f.close()
            os.remove(filepath)
            return restr
    except:
        return ''
