import socket,sys,_thread,select,time,random
from urllib.parse import urlparse

BUFLEN=8192
f=open('proxy.txt','r')
s=f.read()
f.close()
proxylist=s.splitlines()
class Proxy(object):
    def __init__(self,conn,addr):
        self.source=conn
        self.request=""
        self.headers={}
        self.destnation=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.proxy_ip=''
        self.proxy_port=80
        self.run()

    #取协议头
    def get_headers(self):
        header=''
        while True:
            time.sleep(0.1)
            header+=self.source.recv(BUFLEN).decode('utf-8')
            index=header.find('\n')
            if index >0:
                break
        #firstLine,self.request=header.split('\r\n',1)
        firstLine=header[:index]
        self.request=header[index+1:]
        self.headers['method'],self.headers['path'],self.headers['protocol']=firstLine.split()

    #随机取一个代理
    def get_proxy(self):
        proxylen=len(proxylist)
        if proxylen<=0:
            print('没有代理服务器可用!')
            sys.exit()
        pro=proxylist[random.randint(0,proxylen-1)].split(':')
        return (pro[0],int(pro[1]))

    #使用socket去请求网页
    def conn_destnation(self):
        #取请求的ip,端口等信息
        url=urlparse(self.headers['path'])
        hostname=url[1]
        port="80"
        if hostname.find(':') >0:
            addr,port=hostname.split(':')
        else:
            addr=hostname
        port=int(port)
        ip=socket.gethostbyname(addr)
        #self.destnation.connect(('121.69.36.122',8118))

        #循环使用代理连接
        #最多重试次数
        reconnect=0
        while True:
            if reconnect>3:
                break;
            reconnect=reconnect+1
            ipport=[]
            if self.proxy_ip=='':
                ipport=self.get_proxy()
            self.proxy_ip=ipport[0]
            self.proxy_port=ipport[1]
            print('正在连接代理服务器:%s:%s,times:%d'%(self.proxy_ip,self.proxy_port,reconnect))
            try:
                self.destnation.connect((self.proxy_ip,self.proxy_port))
                print('连接成功.\r\n')
                break
            except:
                print('连接代理服务器:%s:%s失败!\r\n准备重试连接...'%(self.proxy_ip,self.proxy_port))
                pass
        data="%s %s %s\r\n" %(self.headers['method'],self.headers['path'],self.headers['protocol'])
        self.destnation.send(bytes(data+self.request,encoding = "utf8"))

        print ("请求目标主机 %s:%d\r\n"%(ip,port))
        print ("请求协议头:\n%s\r\n请求头信息:\n%s\r\n"%(data,self.request))
        # print(self.request.port)

    #把页面转发给原来的请求
    def renderto(self):
        readsocket=[self.destnation]
        while True:
            time.sleep(0.1)
            data=''
            try:
                (rlist,wlist,elist)=select.select(readsocket,[],[],3)
                if rlist:
                    data=rlist[0].recv(BUFLEN)
                    if len(data)>0:
                        self.source.send(data)
                    else:
                        break
            except:
                pass
        #self.proxy_ip=''
        #self.proxy_port=80
        readsocket[0].close();

    def run(self):
        self.get_headers()
        self.conn_destnation()
        self.renderto()



class Server(object):

    #初始化一个套接字接口并监听指定端口
    def __init__(self,host,port,handler=Proxy):
        self.host=host
        self.port=port
        self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host,port))
        self.server.listen(5)
        self.handler=handler

    def start(self):
        print('listening %s:%s'%(self.host,self.port))
        while True:
            time.sleep(1)
            try:
                #接收请求
                conn,addr=self.server.accept()
                _thread.start_new_thread(self.handler,(conn,addr))
            except Exception as e:
                pass


if __name__=='__main__':
    s=Server('127.0.0.1',1225)
    s.start()
