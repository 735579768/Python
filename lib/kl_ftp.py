import ftplib, sys, os ,codecs,kl_log
local_root = 'E:/ftp' 
host = '116.255.214.72' 
username = 'wwwroot' 
passewd = 'adminrootkl' 
faillist=[]
f = False
#定义匿名函数
writeFile = lambda filename: codecs.open(filename, 'w','utf-8').write 
getcwd = lambda curwd: curwd == '/' and '/' or (curwd)#+ '/') 
createDir = lambda dirname: not os.path.exists(dirname) and os.mkdir(dirname)

def isDirectory(filename): 
    try: 
        f.cwd(filename) 
        createDir(local_root+filename) 
        return True 
    except Exception as e:
        #print(e)
        return False 
def recursiveDownload(filelist, curpwd): 
    global local_root 
    global faillist
    for file in filelist:
        if file != '.' and file != '..' :
            try:
                #isDirectory(getcwd(curpwd) + file) and [recursiveDownload(f.nlst(), f.pwd())] or print((getcwd(curpwd) + file)), f.retrlines('RETR '+ (getcwd(curpwd) + file), writeFile(local_root + getcwd(curpwd) + file))
                fol=getcwd(curpwd) + file
                isDirectory(fol) and [recursiveDownload(f.nlst(), f.pwd())] or ( print(fol),f.retrlines('RETR '+fol, writeFile(local_root + fol)))
            except Exception as e:
                faillist.append(e)
                kl_log.log.write("%s"%e)
                print(e)
    


if __name__ == '__main__':
    
    f = ftplib.FTP()
    f.connect(host,2016)
    resp = f.login(username, passewd)
    print(resp)
    print(f.nlst())
    print(f.pwd())
    #进入远程站点根目录
    f.cwd('test') 
    #检查本地根目录有没有创建
    isDirectory('/test')
    #开始下载远程文件
    recursiveDownload(f.nlst(), f.pwd()); 
    f.quit() 
    print('下载失败的文件')
    print(faillist)
    input('请输入任意键结束...')
