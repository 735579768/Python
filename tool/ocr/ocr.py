import os
#curdir=(os.getcwd()+'/').replace('\\','/')

fileimg='E:/Python/tool/ocr/test.png'
fileresult='E:/Python/tool/ocr/result'

command='tesseract '+fileimg+' '+fileresult+' -l httpproxy_mimvp_com_num'
#command=command.replace('[CURDIR]',curdir)
print(command)
os.system(command)

#input('...')