import os,sys
sys.path.append('../../lib/')
#curdir=(os.getcwd()+'/').replace('\\','/')
import kl_lib,kl_download
download=kl_download.kl_download()
download.downfile('http://proxy.mimvp.com/common/ygrandimg.php?id=7&port=Mmzicm4vMpTIz','./','test.png')
fileimg='E:/Python/tool/ocr/test.png'

s=kl_lib.ocr(fileimg,'httpproxy_mimvp_com_num')
print(s)



input('...')
