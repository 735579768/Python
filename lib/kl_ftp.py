import ftplib, os , kl_log, paramiko

#定义匿名函数
#打开一个文件句柄
writeFile = lambda filename:open(filename, 'wb').write
#返回当前目录路径
getcwd = lambda curwd: curwd == '/' and '/' or (curwd)
#创建目录
createDir = lambda dirname: not os.path.exists(dirname) and os.makedirs(dirname)

class kl_ftp:
    def __init__(self,host,port,username,password,ftptype='ftp'):
        self.ftptype=ftptype
        self.ssh=None
        self.sftp=None
        self.ftp = None
        self.ignorefolder=[]
        self.faillist=[]
        self.localroot='./'
        if ftptype=='ftp':
            self.__ftpconn(host,port,username,password)
        else:
            self.__sftpconn(host,username,password)
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

    #定义 ssh 连接函数
    def __sftpconn(self,_host,_username='',_password=''):
        try:
            self.ssh= paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
            self.ssh.connect(_host,username=_username,password=_password)
            self.sftp=self.ssh.open_sftp()
        except Exception as e:
            print( 'ssh %s@%s: %s' % (_username,_host, e) )
            exit()

    #判断是否是目录
    def isDirectory(self,filename):
        try:
            if self.ftptype=='ftp':
                self.ftp.cwd(filename)
            else:
                stdin, stdout, stderr = self.ssh.exec_command(filename)
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
                fol=getcwd(curpwd) + file
                try:
                    #(self.isDirectory(fol) and [self.__recursiveDownload(self.ftp.nlst(), self.ftp.pwd())]) or ( print('downloading...%s'%fol),self.ftp.retrbinary('RETR '+fol, writeFile(local_root + fol),self.ftp.maxline))
                    if self.isDirectory(fol):
                        self.__recursiveDownload(self.ftp.nlst(), self.ftp.pwd())
                    else:
                        print('downloading...%s'%fol)
                        self.ftp.retrbinary('RETR '+fol, writeFile(local_root + fol),self.ftp.maxline)
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
        return True

    #从本地上传文件到远程
    def uploadfile(self,localpath,filepath):
        pass

    #上传本地文件夹到远程
    def uploadfolder(self,localroot,folder):
        pass

    def s_downloadfolder(self,folder,localroot):
        self.localroot=localroot
        createDir(self.localroot)
        self.sftp.get(folder,localroot+'zhaokeli.com.zip')

    def ssh_command(self,command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        relist=[]
        for i in stdout.readlines():
            relist.append(i.strip('\n'))
        print(relist)

    def close(self):
        if self.ftp!=None:
            self.ftp.quit()
        if self.sftp!=None:
            self.sftp.close()
        if self.ssh!=None:
            self.ssh.close()

if __name__ == '__main__':
    # local_root = 'E:/ftp'
    # host = '116.255.214.72'
    # username = 'wwwroot'
    # passewd = 'adminrootkl'
    # ftp=kl_ftp(host,2016,'wwwroot','adminrootkl')
    # ftp.ignorefolder=['Data', 'Public', 'App', 'Plugins', 'TP','dflz.zip']
    # ftp.downloadfolder('test','E:/ftp/')
    # ftp.close()

    #连接ssh服务器
    sftp=kl_ftp('116.255.159.47', 25,'root', 'adminrootkl','sftp')
    #sftp.s_downloadfolder('/var/www/zhaokeli.com.zip', 'E:/sftp/')
    sftp.ssh_command('cd /var/www ; ls -A')
    input('请输入任意键结束...')
