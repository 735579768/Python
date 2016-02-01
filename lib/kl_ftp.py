import ftplib, os ,codecs,kl_log

#定义匿名函数
#打开一个文件句柄
writeFile = lambda filename: codecs.open(filename, 'wb','utf-8').write
#返回当前目录路径
getcwd = lambda curwd: curwd == '/' and '/' or (curwd)
#创建目录
createDir = lambda dirname: not os.path.exists(dirname) and os.makedirs(dirname)

class kl_ftp:
    def __init__(self,host,port,username,password):
        self.ftp = ftplib.FTP()
        self.ignorefolder=[]
        self.faillist=[]
        self.localroot='./'
        self.ftp.maxline=1024*1024*1024
        #f.encoding='UTF-8'#防止中文乱码
        self.ftp.connect(host,port)
        resp = self.ftp.login(username, passewd)
        #输出欢迎信息
        print(resp)
        #初始化日志
        self.log=kl_log.kl_log('kl_ftp')

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
                fol=getcwd(curpwd) + file
                try:
                    (self.isDirectory(fol) and [self.__recursiveDownload(self.ftp.nlst(), self.ftp.pwd())]) or ( print('downloading...%s'%fol),self.ftp.retrlines('RETR '+fol, writeFile(local_root + fol)))
                    #(isDirectory(fol) and [recursiveDownload(self.ftpnlst(), self.ftppwd())]) or ( print('downloading...%s'%fol),self.ftpstorbinary('RETR '+fol, writeFile(local_root + fol)))
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

    def close(self):
        self.ftp.quit()

if __name__ == '__main__':
    local_root = 'E:/ftp'
    host = '116.255.214.72'
    username = 'wwwroot'
    passewd = 'adminrootkl'
    ftp=kl_ftp(host,2016,'wwwroot','adminrootkl')
    ftp.ignorefolder=['Data', 'Public']
    ftp.downloadfolder('test','E:/ftp/')
    ftp.close()
    input('请输入任意键结束...')
