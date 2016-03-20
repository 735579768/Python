import sys,re,random,os,threading,time,_thread
import kl_http,kl_db,kl_reg,kl_progress,kl_log
from urllib.parse import urlparse

log=kl_log.kl_log('spider')
regex=kl_reg
http=kl_http.kl_http()
mylock = _thread.allocate_lock()#线程锁
#mylock.acquire() #Get the lock
#mylock.release()  #Release the lock.
progress=kl_progress.kl_progress('正在采集中')
progress.start()
#最大线程
maxthread=5
threadnum=0
#是否用代理
isproxy=False
http.setproxy('','','127.0.0.1:8087')
db=kl_db.mysql({
            'host':'localhost',
            'user':'root',
            'passwd':'adminrootkl',
            'db':'bokedaquan',
            'prefix':'kl_',
            'charset':'utf8'
        })
prooxypath='../proxy/proxy.txt'
proxylist=[]
if os.path.exists(prooxypath):
    f=open('../proxy/proxy.txt','r')
    s=f.read()
    f.close()
    proxylist=s.splitlines()

class urlspider(object):
    """docstring for urlspider"""
    def __init__(self, arg):
        super(urlspider, self).__init__()
        self.arg = arg
        self.hostname=arg['hostname']
        self.linkreg='<a[^><\n]*?href=["|\']{0,1}([^><\n]*?(?:00_00)[^><\n]*?)["|\']{0,1}[^><\n]*?>.*?</a>'
        self.url=arg['url']
        self.charset=arg['charset']
        self.mb_url_reg=arg['mb_url_reg']
        self.mb_con_reg=arg['mb_con_reg']
        self.link_tezheng=arg['link_tezheng']
        self.shendu=int(arg['shendu'])
        self.url_table=arg['name']+'_url'
        self.content_table=arg['name']+'_content'
        self.urled_table=arg['name']+'_urled'
        self.content_sql=arg['content_sql']
        self.init()

    #创建数据表
    def init(self):
        #创建已经采集的url数据表
        sql='''\
CREATE TABLE `[TABLE]` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=77089 DEFAULT CHARSET=utf8;'''
        sql=sql.replace('[TABLE]',db.prefix+self.urled_table)
        db.query(sql);
        #创建url数据表
        sql='''\
CREATE TABLE `[TABLE]` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(255) DEFAULT NULL,
  `src_url` varchar(255) DEFAULT NULL,
  `hostname` varchar(255) DEFAULT NULL,
  `update_time` int(11) DEFAULT NULL,
  `status` smallint(3) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=77089 DEFAULT CHARSET=utf8;'''
        sql=sql.replace('[TABLE]',db.prefix+self.url_table)
        db.query(sql);
        #创建content内容数据表
        sql='''\
CREATE TABLE `[TABLE]` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
    [CONTENT_SQL]
  `src_url` varchar(255) DEFAULT NULL,
  `update_time` int(11) DEFAULT NULL,
  `status` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=77089 DEFAULT CHARSET=utf8;'''
        sql=sql.replace('[TABLE]',db.prefix+self.content_table)
        sql=sql.replace('[CONTENT_SQL]',self.content_sql)
        db.query(sql);

    def run(self):
        self.shenduurl(self.url)
        self.caijicon()

    #随机取一个代理
    def get_proxy(self):
        proxylen=len(proxylist)
        if proxylen<=0:
            print('There is no available proxy server!')
            sys.exit()
        while True:
            pro=proxylist[random.randint(0,proxylen-1)]
            if pro!="":
                return pro

    def shenduurl(self,url,cur_shendu=1):
        result=db.table(self.urled_table).where({'url':url}).count()
        if result>0:
            return True
        global  threadnum
        global  maxthread
        global isproxy
        threadnum+=1
        print("collection page %s depth:%d"%(url,cur_shendu))
        ht=kl_http.kl_http()
        ht.autoUserAgent=True
        r=None
        while True:
            if isproxy:
                daili=self.get_proxy()
                print("using proxy:%s"%daili)
                http.resetsession()
                http.setproxy('','',daili)
            r=http.geturl(url)
            if http.lasterror==None:
                break
            else:
                print(http.lasterror)
        if r!=None:
            content=r.read().decode(self.charset)
            #查找目标url
            mburl_list=regex.findall(self.mb_url_reg,content, regex.I|regex.S)
            #去重
            mburl_list = list(set(mburl_list))
            mylock.acquire()
            self.adddata(mburl_list,url)
            mylock.release()
            #深度查找
            if cur_shendu<self.shendu:
                cur_shendu+=1
                xiangsereg=self.linkreg.replace('00_00',self.link_tezheng)
                sdurl_list=regex.findall(xiangsereg,content, regex.I|regex.S)
                sdurl_list = list(set(sdurl_list))
                for j in sdurl_list:
                    while True:
                        if threadnum<maxthread:
                            threading.Thread(target=self.shenduurl,args=(self.formaturl(url,j),cur_shendu,)).start()
                            break
                        time.sleep(1)

        #添加已经采集过的网址
        db.table(self.urled_table).add({'url':url})
        threadnum-=1

     #下面开始采集内容
    def caijicon(self):
        while 1:
            dlist=db.table(self.url_table).limit(10).order('id asc').where({
                'status':0
                }).getarr()
            if not dlist:
                break
            for i in dlist:
                url=self.formaturl(i['src_url'],i['url'])
                print("collection page %s"%(url))
                ht=kl_http.kl_http()
                ht.autoUserAgent=True
                r=None
                while True:
                    if isproxy:
                        daili=self.get_proxy()
                        print("using proxy:%s"%daili)
                        http.resetsession()
                        http.setproxy('','',daili)
                    r=http.geturl(url)
                    if http.lasterror==None:
                        break
                    else:
                        print(http.lasterror)
                if r!=None:
                    content=r.read().decode(self.charset)
                    #查找目标url
                    mbcon_list=regex.findall(self.mb_con_reg,content, regex.I|regex.S)
                    #去重
                    mbcon_list = list(set(mbcon_list))
                    print(mbcon_list)
                    db.table(self.url_table).where({'id':i['id']}).save({'status':r.code})

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
    #添加数据到数据库
    def adddata(self,urllist,src_url):
        for i in urllist:
            result=db.table(self.url_table).where({
                'hostname':self.hostname,
                'url':i
                }).count()
            if result<1:
                res=db.table(self.url_table).add({
                    'url':i,
                    'hostname':self.hostname,
                    'status':0,
                    'update_time':time.time(),
                    'src_url':src_url
                    })
                if res<=0:
                    log.write('add %s error:%s'%(i,db.lasterror))
                    log.write('lastsql:%s'%db.getlastsql())
                else:
                    print("add url：%s"%i)




#链接url正则
cjurl=[
    {
    #采集项目的名字
    'name':'boke',
    'hostname':'http://lusongsong.com',
    #入口地址
    'url':'http://lusongsong.com/daohang/',
    #抓取进入的深度
    'shendu':2,
    #类似网址入口正则(精确要进入采集的网址)
    'link_tezheng':'\/daohang\/webdir\-[^><\n]*?\.html',
    #目标网址正则
    'mb_url_reg':'<a[^><\n]*?href=["|\']?([^><\n]*?(?:showurl_\d+?\.html)[^><\n]*?)["|\']?[^><\n]*?>.*?</a>',
    #目标内容正则
    'mb_con_reg':'点此打开.*?【(.*?)】.*?网址.*?<a.*?href="(.*?)".*?>.*?</a>',
    #内容正则中的分组对应的字段信息
    'field':{
        'title':1,
        'url':2,
        'descr':3,
        'area':4,
        'blog_type':5
    },
    #采集到的内容字段sql语句
    'content_sql':'''\
              `title` varchar(255) DEFAULT NULL,
              `url` varchar(255) DEFAULT NULL,
              `descr` varchar(255) DEFAULT NULL,
              `area` varchar(255) DEFAULT NULL,
              `blog_type` varchar(255) DEFAULT NULL,''',
    'charset':'utf-8',
    }
]

for i in cjurl:
    urlspider(i).run()


while True:
    if threadnum==0:
        progress.stop()
        break
    time.sleep(1)



input('it is conllected,please press any key to continue...')
