import os
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
