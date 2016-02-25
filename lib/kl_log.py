import os
import time
class kl_log:
    def __init__(self,filename='kl_log'):
        self.filename=filename+'-'
        self.filepath='./data/log/'

    def setpath(self,filepath):
        self.filepath=filepath

    def setfilename(self,filename):
        self.filename=filename+'-'

    def write(self,data='',model='a'):
        fname=time.strftime('%Y-%m-%d',time.localtime())
        fpath='%s%s%s.log'%(self.filepath,self.filename,fname)
        if os.path.exists(os.path.dirname(fpath))==False :
            os.makedirs(os.path.dirname(fpath))

        ti=time.strftime('%Y-%m-%d %X',time.localtime())
        f=open(fpath,model)
        f.write("%s: %s\n"%(ti,data))
        f.close()
        return True

if __name__ == '__main__':
    log=kl_log('app')
    log.write('aaaaaa')
    os.system("pause")
