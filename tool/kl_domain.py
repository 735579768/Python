import kl_spider
#链接url正则
cjurl=[
    {
    #采集项目的名字
    'name':'domain',
    'hostname':'http://del.chinaz.com/',
    #入口地址
    'url':'http://del.chinaz.com/?kw=&p=0&bl=6&el=6&ds%5B%5D=1&py=1&pl=0&sort=1&suffix%5B%5D=com&dt=1&date=1&pagesize=30&st=1&page=1',
    #抓取进入的深度
    'shendu':0,
    #类似网址入口正则(精确要进入采集的网址)
    'link_tezheng':['/\?kw\=&p\=0&bl\=6&el\=6&ds%5B%5D\=1&py\=1&pl\=0&sort\=1&suffix%5B%5D\=com&dt\=1&date\=1&pagesize\=30&st\=1&page\=\d{1,5}'],
    #目标网址正则
    'mb_url_reg':'<a[^><\n]*?href=["|\']?([^><\n]*?(?:/\?kw\=&p\=0&bl\=6&el\=6&ds%5B%5D\=1&py\=1&pl\=0&sort\=1&suffix%5B%5D\=com&dt\=1&date\=1&pagesize\=30&st\=1&page\=\d{1,5})[^><\n]*?)["|\']?[^><\n]*?>.*?</a>',
    #目标内容正则
    'mb_con_reg':'<td[^>]*?domainname.*?>.*?(<a[^>]*?>(\w{6,6}\.com).*?</a>).*?</td>',
    #内容正则中的分组对应的字段信息
    'field':{
        'domain':2,
    },
    #采集到的内容字段sql语句
    'content_sql':'''\
              `domain` varchar(255) DEFAULT NULL,''',
    'charset':'utf-8',
    }
]

for i in cjurl:
    spi=kl_spider.urlspider(i)
    spi.run()
#input('it is conllected,please press any key to continue...')