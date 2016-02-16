import sys,re,random
sys.path.append('../../lib/')
import kl_http,kl_db,kl_reg
regex=kl_reg
http=kl_http.kl_http()
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
    'link_tezheng':'\/daohang\/webdir\-.*?\.html',
    'mb_url_reg':'<a.*?href=["|\']{0,1}(.*?(?:showurl_\d+?\.html).*?)["|\']{0,1}.*?>.*?</a>',
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
        self.linkreg='<a.*?href=["|\']{0,1}(.*?(?:00_00).*?)["|\']{0,1}.*?>.*?</a>'
        self.url=arg['url']
        self.charset=arg['charset']
        self.mb_url_reg=arg['mb_url_reg']
        self.mb_url_reg=arg['mb_url_reg']
        self.link_tezheng=arg['link_tezheng']
        self.shendu=int(arg['shendu'])

    def run(self):
        self.shenduurl(self.url)

    def shenduurl(self,url,cur_shendu=1):
        r=http.geturl(url)
        if r!=None:
            content=r.read().decode(self.charset)
            #查找目标url
            mburl_list=regex.findall(self.mb_url_reg,content, regex.I)

            #深度查找
            if cur_shendu<=self.shendu:
                xiangsereg=self.linkreg.replace('00_00',self.link_tezheng)
                sdurl_list=regex.findall(xiangsereg,content, regex.I)
                for j in sdurl_list:
                    self.shenduurl(self.hostname+j,cur_shendu+1)


for i in cjurl:
    urlspider(i).run()






input('输入任意键继续...')
