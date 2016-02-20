import urllib.request
import sys
import os
import threading
#创建目录
def create_dir(dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

def callbackfunc(blocknum, blocksize, totalsize):
    '''回调函数
    @blocknum: 已经下载的数据块
    @blocksize: 数据块的大小
    @totalsize: 远程文件的大小
    '''
    global url
    percent = 100.0 * blocknum * blocksize / totalsize
    if percent >= 100:
        percent = 100
    downsize=blocknum * blocksize
    if downsize >= totalsize:
    	downsize=totalsize
    if __name__ == "__main__":
        s ="%.2f%%=>%.2f B/%.2f B \r"%(percent,downsize,totalsize)
        sys.stdout.write(s)
        sys.stdout.flush()
    if percent == 100:
        print('')
        return True

def downfile(url,outdir):
    filename=os.path.basename(url)
    try:
        create_dir(outdir)
    except:
        pass
    filepath=outdir+'/'+filename
    urllib.request.urlretrieve(url, filepath, callbackfunc)

if __name__ == "__main__":
    url='http://dlsw.baidu.com/sw-search-sp/soft/e7/10520/KanKan_V2.7.8.2126_setup.1416995191.exe'
    outdir="./downs"
    downfile(url,outdir)

    #启动线程下载
    #threading.Thread(target=downfile,args=(url,outdir,)).start()
    input('下载完毕')
