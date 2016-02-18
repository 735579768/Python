import sys,re,random
sys.path.append('../../lib/')
import kl_http,kl_db
http=kl_http.kl_http()
http.setproxy('','','127.0.0.1:8087')
db=kl_db.mysql({
            'host':'localhost',
            'user':'root',
            'passwd':'adminrootkl',
            'db':'douban',
            'prefix':'kl_',
            'charset':'utf8'
        })
http.autoUserAgent=True

try:
	for m in range(1989,2000,1):
		for n in range(0,550,15):
			reurl='http://www.douban.com/tag/%s/movie?start=%s'%(m,n)
			print(reurl)
			r=http.geturl(reurl).read().decode()
			http.resetsession()
			#查找电影列表
			data=re.findall('movie\-list[\s\S]*?paginator', r,re.S|re.I)

			#查找单个电影
			restr='dl[ALL]<a.*?href="(.*?)"[ALL]</a>[ALL]<a.*?>([ALL])</a>[ALL]</dl'
			restr=restr.replace('[ALL]', '[\s\S]*?')
			item=re.findall(restr, data[0])
			for i in item:
				lis=db.table('url').where("url='"+i[0]+"'").select()
				lis=lis.fetchall()
				if len(lis)<=0:
					db.table('url').add({
						'url':i[0],
						'title':i[1],
						'urltype':'douban'
						})
					print("添加一个新影片:【%s】  %s"%(i[0],i[1]))
except:
	pass
input('输入任意键继续...')
