import os,sys
sys.path.append('../../lib/')
#curdir=(os.getcwd()+'/').replace('\\','/')
import kl_lib

fileimg='E:/Python/tool/ocr/test.png'

#s=kl_lib.ocr(fileimg,'httpproxy_mimvp_com_num')
s=kl_lib.ocr(fileimg)
print(s)



input('...')