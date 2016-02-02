'''
+----------------------------------------------------------------------
// | Author: 赵克立 <735579768@qq.com> <http://www.zhaokeli.com>
// |mysql数据库操作类
+----------------------------------------------------------------------
// |远程和本地目录以不要 "/" 结尾
'''
import ftplib, os , kl_log, paramiko
from Queue import Queue
queue = Queue()
#定义匿名函数
#打开一个文件句柄
writeFile = lambda filename:open(filename, 'wb').write
#创建目录
createDir = lambda dirname: not os.path.exists(dirname) and os.makedirs(dirname)

class kl_ftp:
    def __init__(self,host,port,username,password):
        self.ftp = None
        self.ignorefolder=[]
        self.faillist=[]
        self.localroot='./'
        self.__ftpconn(host,port,username,password)
        #初始化日志
        self.log=kl_log.kl_log('kl_ftp')

    def __ftpconn(self,host,port,username,password):
        self.ftp=ftplib.FTP()
        #最大1G文件
        self.ftp.maxline=1024*1024*1024
        #f.encoding='UTF-8'#防止中文乱码
        self.ftp.connect(host,port)
        resp = self.ftp.login(username, password)
        #输出欢迎信息
        print(resp)

    #判断是否是目录
    def isDirectory(self,filename):
        try:
            self.ftp.cwd(filename)
            createDir(self.localroot+filename)
            return True
        except ftplib.error_perm as e:
            #如果不是目录会报错并返回False
            #print(e)
            return False

    #下载ftp文件
    def __recursiveDownload(self,filelist, curpwd):
        for file in filelist:
            if file != '.' and file != '..' :
                if file in self.ignorefolder:
                    continue
                fol=curpwd + file
                try:
                    if self.isDirectory(fol):
                        self.__recursiveDownload(self.ftp.nlst(), self.ftp.pwd())
                    else:
                        localpath=self.localroot + fol
                        print('downloading...%s ----> %s'%(fol, localpath))
                        self.ftp.retrbinary('RETR '+fol, writeFile(localpath),self.ftp.maxline)
                except Exception as e:
                    print(e)
                    self.faillist.append(fol)
                    self.log.write("Error:%s"%e)
                    self.log.write("%s"%e)


    #从远程下载单个文件到本地
    def downloadfile(self,filepath,localpath):
        pass

    #下载远程文件夹到本地
    def downloadfolder(self,folder,localroot):
        if self.ftp:
            self.localroot=localroot
            self.ftp.cwd(folder)
            createDir(self.localroot+folder)
            self.__recursiveDownload(self.ftp.nlst(), self.ftp.pwd());
        self.log.write("下载错误的文件:%s"%self.faillist)
        print('下载错误的文件:')
        print(self.faillist)
        return True

    #从本地上传文件到远程
    def uploadfile(self,localpath,filepath):
        pass

    #上传本地文件夹到远程
    def uploadfolder(self,localroot,folder):
        pass

    def close(self):
        if self.ftp!=None:
            self.ftp.quit()

class kl_sftp:
    def __init__(self,host,port,username,password):
        self.ssh=None
        self.sftp=None
        self.ignorefolder=[]
        self.faillist=[]
        self.localroot='./'
        self.__sftpconn(host,username,password)
        #初始化日志
        self.log=kl_log.kl_log('kl_sftp')

    #定义 ssh 连接函数
    def __sftpconn(self,_host,_username='',_password=''):
        try:
            self.ssh= paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
            self.ssh.connect(_host,username=_username,password=_password)
            self.sftp=self.ssh.open_sftp()
            self.sftp.chdir('/')
            print('当前目录:%s'%self.sftp.getcwd())
        except Exception as e:
            print( 'ssh %s@%s: %s' % (_username,_host, e) )
            exit()

    #判断是否是目录
    def isDirectory(self,filename):
        try:
            self.sftp.chdir(filename)
            createDir(self.localroot+filename)
            return True
        except Exception as e:
            #如果不是目录会报错并返回False
            #print(e)
            return False

    #从远程下载单个文件到本地
    def downloadfile(self,filepath,localpath):
        pass

    #从本地上传文件到远程
    def uploadfile(self,localpath,filepath):
        pass

    #上传本地文件夹到远程
    def uploadfolder(self,localroot,folder):
        pass
    def __downfilelist(self,filelist, curpwd):
        for file in filelist:
             if file != '.' and file != '..' :
                if file in self.ignorefolder:
                    continue
                fol=curpwd +'/'+ file
                try:
                    if self.isDirectory(fol):
                        self.__downfilelist(self.sftp.listdir(), self.sftp.getcwd())
                    else:
                        localpath=self.localroot+fol
                        print('downloading...%s ----> %s'%(fol, localpath))
                        self.sftp.get(fol,localpath)
                except Exception as e:
                    print(e)
                    self.faillist.append(fol)
                    self.log.write("Error:%s"%e)
                    self.log.write("%s"%e)


    def downloadfolder(self,folder,localroot):
        if self.sftp:
            self.localroot=localroot
            self.sftp.chdir(folder)
            createDir(self.localroot+folder)
            self.__downfilelist(self.sftp.listdir(), self.sftp.getcwd());
        self.log.write("下载错误的文件:%s"%self.faillist)
        print('下载错误的文件:')
        print(self.faillist)
        return True

    def ssh_command(self,command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        relist=[]
        for i in stdout.readlines():
            relist.append(i.strip('\n'))
        print(relist)

    def close(self):
        if self.sftp!=None:
            self.sftp.close()
        if self.ssh!=None:
            self.ssh.close()


if __name__ == '__main__':
    print('请输入用户名:')
    username=input()
    print('请输入密码:')
    password=input()
    #连接ftp服务器
    ftp=kl_ftp('116.255.214.72',2016,username,password)
    ftp.ignorefolder=['Data', 'Public', 'App', 'Plugins', 'TP','dflz.zip']
    ftp.downloadfolder('test','E:/ftp')
    ftp.close()

    #连接ssh服务器
    sftp=kl_sftp('116.255.159.47', 22,'root', password)
    sftp.ignorefolder=['Data', 'Public', 'App', 'Plugins', 'TP','zhaokeli.com.zip']
    sftp.downloadfolder('/var/www/zhaokeli.com', 'E:/sftp')
    sftp.close()
    input('请输入任意键结束...')
