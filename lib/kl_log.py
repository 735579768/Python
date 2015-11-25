import sys
import os
import time
class log:
    def __init__(self):
        pass
    
    #get取网页数据
    def write(filepath,data,model='a'):
        if os.path.exists(os.path.dirname(filepath))==False :
            os.makedirs(os.path.dirname(filepath))
        ti=time.strftime('%Y-%m-%d %X',time.localtime())
        f=open(filepath,model)
        f.write("%s:%s\r"%(ti,data))
        f.close()
        
        return True
if __name__ == '__main__':
	log.write('./log/run.log','aaaaaa')
	input('按任意键继续...')
