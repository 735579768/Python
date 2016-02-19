from pytesseract import *
from PIL import Image
import os
curdir=(os.getcwd()+'/').replace('\\','/')

command='''\
cd /d [CURDIR]
tesseract test.png result -l num\
'''
command=command.replace('[CURDIR]',curdir)
os.system(command)

input('...')