#-------------------------------------------------------------------------------
# Name:        PortScan
# Purpose:     扫描目标主机的端口开放情况
#-------------------------------------------------------------------------------
import socket,sys,threading,os
def main(ip,scanport):
    global xcnum
    xcnum=xcnum+1

    for port in scanport:
        sys.stdout.write('正在扫描：%s : %d\r' %(ip,port))
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
if __name__ == '__main__':
    #常见的开放端口
    scanport=[20,21,22,25,3306,3389]
    ip=input('请输入目标主机段：(默认:116.255.214)')
    if ip=='':
        ip='116.255.214'
    ipnum=0
    xcnum=0
    filepath='./data/scan/%s---.txt'%ip
    if os.path.exists(os.path.dirname(filepath))==False :
        os.makedirs(os.path.dirname(filepath))
    f=open(filepath,'a')
    while ipnum<255 :
        if xcnum<5000 :
            threading.Thread(target=main,args=("%s.%s"%(ip,ipnum),scanport)).start()
            ipnum=ipnum+1
    while xcnum != 0:
        pass
    f.close()
    print('扫描完毕')
    input('输入任意键继续...')
