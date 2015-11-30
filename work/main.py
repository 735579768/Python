import functions
import threading
import codecs
import re
h=functions
def getpage(url=''):
	html = h.geturl(u"http://www.0yuanwang.com")
	print(type(html))
	f=codecs.open('test.txt','a','utf-8')
	print(html.__class__)
	html=re.sub(r'(<style.*?>[\s\S]*?</style>)|(<script.*?>[\s\S]*?</script>)|(<[\s\S]*?>)|(\s*)','',html.decode('utf-8'))
	#print(html)
	f.write(html)
	f.close()

threads = []
t1 = threading.Thread(target=getpage,args=('')).start()
#threads.append(t1)
#t1.start()

input('按任意键继续...')
