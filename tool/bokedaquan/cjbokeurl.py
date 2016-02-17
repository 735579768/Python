import sys,re,random,os
sys.path.append('../../lib/')
import kl_http,kl_db,kl_reg
from urllib.parse import urlparse
regex=kl_reg
http=kl_http.kl_http()
#最大线程
maxthread=10
threadnum=0
http.setproxy('','','127.0.0.1:8087')
db=kl_db.mysql({
            'host':'localhost',
            'user':'root',
            'passwd':'adminrootkl',
            'db':'bokedaquan',
            'prefix':'kl_',
            'charset':'utf8'
        })
#链接url正则
cjurl=[
    {
    'hostname':'http://lusongsong.com',
    'url':'http://lusongsong.com/daohang/',
    'shendu':2,
    'link_tezheng':'\/daohang\/webdir\-[^><\n]*?\.html',
    'mb_url_reg':'<a[^><\n]*?href=["|\']{0,1}([^><\n]*?(?:showurl_\d+?\.html)[^><\n][^><\n]*?)["|\']{0,1}.*?>.*?</a>',
    'mb_con_reg':'点此打开.*?【(.*?)】.*?网址.*?<a.*?href="(.*?)".*?>.*?</a>',
    'charset':'utf-8',
    }
]
class urlspider(object):
    """docstring for urlspider"""
    def __init__(self, arg):
        super(urlspider, self).__init__()
        self.arg = arg
        self.hostname=arg['hostname']
        self.linkreg='<a[^><\n]*?href=["|\']{0,1}([^><\n]*?(?:00_00)[^><\n]*?)["|\']{0,1}.*?>.*?</a>'
        self.url=arg['url']
        self.charset=arg['charset']
        self.mb_url_reg=arg['mb_url_reg']
        self.mb_url_reg=arg['mb_url_reg']
        self.link_tezheng=arg['link_tezheng']
        self.shendu=int(arg['shendu'])

    def run(self):
        self.shenduurl(self.url)

    def shenduurl(self,url,cur_shendu=1):
        print("%s 深度:%d"%(url,cur_shendu))
        r=http.geturl(url)
        if r!=None:
            content=r.read().decode(self.charset)
            #查找目标url
            mburl_list=regex.findall(self.mb_url_reg,content, regex.I)
            mburl_list = list(set(mburl_list))

            #深度查找
            if cur_shendu<self.shendu:
                cur_shendu+=1
                xiangsereg=self.linkreg.replace('00_00',self.link_tezheng)
                sdurl_list=regex.findall(xiangsereg,content, regex.I)
                sdurl_list = list(set(sdurl_list))
                for j in sdurl_list:
                    self.shenduurl(self.formaturl(url,j),cur_shendu)
                cur_shendu-=1

    #格式化请求的路径
    def formaturl(self,requestpath,curpath):
        #请求的url目录
        urldir=os.path.dirname(requestpath)
        url=urlparse(requestpath)
        protocol=url[0]
        hostname=url[1]
        if curpath[0:1]=='/':
            return '%s://%s%s'%(protocol,hostname,curpath)
        else:
            return urldir+'/'+curpath

for i in cjurl:
    urlspider(i).run()






input('输入任意键继续...')
