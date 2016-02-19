from pytesseract import *
from PIL import Image

image_file='E:/Python/tool/proxy/ygrandimg.png'
im = Image.open(image_file)
#text = image_to_string(im)
text = image_to_string(im,lang='fra')
#text = image_file_to_string(image_file, graceful_errors=True)
print ("=====output=======")
print (text)

input('...')