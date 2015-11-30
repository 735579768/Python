import sys
import os
import time
def write(data='',model='a',filepath=''):
    if filepath =='':
        filename=time.strftime('%Y-%m-%d',time.localtime())
        filepath='./data/log/'+filename+'.log'
    if os.path.exists(os.path.dirname(filepath))==False :
        os.makedirs(os.path.dirname(filepath))
    ti=time.strftime('%Y-%m-%d %X',time.localtime())
    f=open(filepath,model)
    f.write("%s: %s\r\n"%(ti,data))
    f.close()
    return True
if __name__ == '__main__':
	write('aaaaaa')
	input('按任意键继续...')
