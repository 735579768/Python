#-------------------------------------------------------------------------------
# Name:        PortScan
# Purpose:     扫描目标主机的端口开放情况
#-------------------------------------------------------------------------------
import socket,sys,threading,os
def main(ip,port):
    global xcnum,f
    xcnum=xcnum+1
    sys.stdout.write('正在扫描端口：%d\r' % port)
    sys.stdout.flush()
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(1000)
    try:
        result=sk.connect((ip,port))
        print('Server %s port %d OK!' % (ip,port))
        f.write("%s : %s \r\n"%(ip,port))
    except Exception:      
        pass
    sk.close()
    xcnum=xcnum-1
    if xcnum == 0 :
        f.close()
if __name__ == '__main__':
    ip=input('请输入目标主机：(默认:116.255.214.72)')
    if ip=='':
        ip='116.255.214.72'
    s=input('请输入目标主机开始端口：(默认:20)')
    if s=='':
        startport=20
    else:
        startport=int(s)

    s=input('请输入目标主机结束端口：(默认:65535)')
    if s=='':
        endport=65535
    else:
        endport=int(s)
    xcnum=0
    filepath='./data/scan/%s-port.txt'%ip
    if os.path.exists(os.path.dirname(filepath))==False :
        os.makedirs(os.path.dirname(filepath))
    f=open(filepath,'a')
    while startport<=endport :
        if xcnum<5000 :
            threading.Thread(target=main,args=(ip,startport)).start()
            startport=startport+1
    if startport==endport :
        sys.stdout.write('扫描完毕')
        sys.stdout.flush()
        print('')
        input('输入任意键继续...')
