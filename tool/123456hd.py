from kl_spider import urlspider
#链接url正则
cjurl=[
    {
    #采集项目的名字
    'name':'moviebt',
    'hostname':'http://www.123456hd.com',
    #入口地址
    'url':'http://123456hd.com/1_2____datetime_.html',
    #抓取进入的深度
    'shendu':3,
    #类似网址入口正则(精确要进入采集的网址)
    'link_tezheng':['/\d{1,5}_\d{1,5}____datetime_\.html','/\d{1,5}_\d{1.5}____datetime_\.html'],
    #目标网址正则
    'mb_url_reg':'<a[^><\n]*?href=["|\']?(/detail/\?\d{1,10}\.html)["|\']?[^><\n]*?>.*?</a>',
    #目标内容正则
    'mb_con_reg':'layout_fbox.*?影片名称.*?<strong>(.*?)</strong>.*?第1集.*?href\="(.*?)".*?</li>',
    #内容正则中的分组对应的字段信息
    'field':{
        'title':1,
        'moviebt':2
    },
    #采集到的内容字段sql语句
    'content_sql':'''\
              `title` varchar(255) DEFAULT NULL,
              `moviebt` varchar(255) DEFAULT NULL,''',
    'charset':'gbk',
    }
]

for i in cjurl:
    spi=urlspider(i)
    spi.isproxy=True
    spi.run()





input('it is conllected,please press any key to continue...')