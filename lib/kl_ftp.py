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
                fol=getcwd(curpwd) + file
                try:
                    (self.isDirectory(fol) and [self.__recursiveDownload(self.ftp.nlst(), self.ftp.pwd())]) or ( print('downloading...%s'%fol),self.ftp.retrlines('RETR '+fol, writeFile(local_root + fol)))
                    #(isDirectory(fol) and [recursiveDownload(self.ftpnlst(), self.ftppwd())]) or ( print('downloading...%s'%fol),self.ftpstorbinary('RETR '+fol, writeFile(local_root + fol)))
                except Exception as e:
                    print(e)
                    self.faillist.append(fol)
                    self.log.write("Error:%s"%e)
                    self.log.write("%s"%e)

    def downloadfold(self,folder,localroot):
        if self.ftp:
            self.localroot=localroot
            self.ftp.cwd(folder)
            self.__recursiveDownload(self.ftp.nlst(), self.ftp.pwd());
        return True

    def close(self):
        self.ftp.quit()


log=kl_log.kl_log('ftp')
local_root = 'E:/ftp'
host = '116.255.214.72'
username = 'wwwroot'
passewd = 'adminrootkl'
faillist=[]
f = False


#判断是否是目录
def isDirectory(filename):
    try:
        f.cwd(filename)
        createDir(local_root+filename)
        return True
    except ftplib.error_perm as e:
        #如果不是目录会报错并返回False
        #print(e)
        return False

#下载ftp文件
def recursiveDownload(filelist, curpwd):
    global local_root
    global faillist
    for file in filelist:
        if file != '.' and file != '..' :
            fol=getcwd(curpwd) + file
            try:
                (isDirectory(fol) and [recursiveDownload(f.nlst(), f.pwd())]) or ( print('downloading...%s'%fol),f.retrlines('RETR '+fol, writeFile(local_root + fol)))
                #(isDirectory(fol) and [recursiveDownload(f.nlst(), f.pwd())]) or ( print('downloading...%s'%fol),f.storbinary('RETR '+fol, writeFile(local_root + fol)))
            except Exception as e:
                print(e)
                faillist.append(fol)
                log.write("Error:%s"%e)
                log.write("%s"%e)



if __name__ == '__main__':

    # f = ftplib.FTP()
    # f.maxline=81920
    # #f.encoding='UTF-8'#防止中文乱码
    # f.connect(host,2016)
    # resp = f.login(username, passewd)
    # #输出欢迎信息
    # print(resp)

    # #输出当前目录列表(包含文件)
    # print(f.nlst())

    # #输出当前目录路径
    # print(f.pwd())

    # #进入远程站点根目录
    # f.cwd('test')

    # print(f.pwd())
    # print(f.nlst())

    # #检查本地根目录有没有创建
    # isDirectory('/test')
    # #开始下载远程文件
    # recursiveDownload(f.nlst(), f.pwd());
    # f.quit()
    # print('下载失败的文件')
    # print(faillist)
    local_root = 'E:/ftp'
    host = '116.255.214.72'
    username = 'wwwroot'
    passewd = 'adminrootkl'
    ftp=kl_ftp(host,2016,'wwwroot','adminrootkl')
    ftp.downloadfold('test','E:/ftp')
    input('请输入任意键结束...')
