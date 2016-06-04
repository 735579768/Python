import os,tempfile,time,subprocess
from urllib.parse import urlparse
from colorama import init,Fore, Back, Style
import re
from kl_print  import *

init(autoreset=True)
A=re.A
DEBUG=re.DEBUG
I=re.I
L=re.L
M=re.M
S=re.S
X=re.X
########匿名函数###################
write_file = lambda filename:open(filename, 'wb').write
#创建目录
create_dir = lambda dirname: not os.path.exists(dirname) and os.makedirs(dirname)


#格式化网页资源请求的路径
def format_url(self,requestpath,curpath):
    #请求的url目录
    urldir=os.path.dirname(requestpath)
    url=urlparse(requestpath)
    protocol=url[0]
    hostname=url[1]
    if curpath[0:1]=='/':
        return '%s://%s%s'%(protocol,hostname,curpath)
    else:
        return urldir+'/'+curpath

#ocr识别,需要系统中安装tesseract-ocr并将路径添加到系统路径中
def ocr(imgpath,lang=''):
    temp=tempfile.NamedTemporaryFile()
    temppath=temp.name
    temp.close()
    try:
        if lang:
            lang=' -l %s'%lang
        command='tesseract %s %s %s'%(imgpath,temppath,lang)
        resu=subprocess.call(command, shell=True)
        if not  resu:
            filepath=temppath+'.txt'
            f=open(filepath,'r')
            restr=f.read().replace('\n','')
            f.close()
            os.remove(filepath)
            return restr
    except:
        return ''

#正则替换字符串
def reg_replace(pattern,replacement,subject,flags=0):
    try:
        p = re.compile(pattern,flags)
        return p.sub(replacement,subject)
    except Exception as e:
        print_red('[ERROR]:%s  [REGEX]:%s'%(e, pattern))
        print()
        return ()

#正则替换,返回替换的数量
def reg_replacenum(pattern,replacement,subject,flags=0):
    try:
        p = re.compile(pattern,flags)
        return p.subn(replacement,subject)
    except Exception as e:
        print_red('[ERROR]:%s  [REGEX]:%s'%(e, pattern))
        print()
        return ()

#从字符串中查找匹配,匹配失败返回None,成功默认返回第一个匹配,如果想完全匹配请在正则上加上$，这时就跟fullmatch一样
def reg_match(pattern,subject,pos=0,endpos=0,flags=0):
    try:
        endpos =len(subject)
        p = re.compile(pattern,flags)
        return p.match(subject)
    except Exception as e:
        print_red('[ERROR]:%s  [REGEX]:%s'%(e, pattern))
        print()
        return ()

#匹配整个字符串,匹配失败返回None
def reg_fullmatch(pattern,subject,pos=0,endpos=0,flags=0):
    try:
        endpos =len(subject)
        p = re.compile(pattern,flags)
        return p.fullmatch(subject,pos,endpos)
    except Exception as e:
        print_red('[ERROR]:%s  [REGEX]:%s'%(e, pattern))
        print()
        return ()

#搜索失败返回None,成功返回一个match对象,可以使用match.group([num])取分组信息
def reg_search(pattern,subject,pos=0,endpos=0,flags=0):
    try:
        endpos=len(subject)
        p = re.compile(pattern,flags)
        return p.search(subject,pos,endpos)
    except Exception as e:
        print_red('[ERROR]:%s  [REGEX]:%s'%(e, pattern))
        print()
        return ()

#按照能够匹配的子串将subject分割后返回列表。
def reg_split(pattern,subject,flags=0):
    try:
        p = re.compile(pattern,flags)
        return p.split(subject)
    except Exception as e:
        print_red('[ERROR]:%s  [REGEX]:%s'%(e, pattern))
        print()
        return ()

#搜索string，以列表形式返回全部能匹配的子串。
def reg_findall(pattern,subject,flags=0):
    try:
        p =re.compile(pattern,flags)
        return p.findall(subject)
    except Exception as e:
        print_red('[ERROR]:%s  [REGEX]:%s'%(e, pattern))
        print()
        return ()

#搜索string，返回一个顺序访问每一个匹配结果（Match对象）的迭代器。
def reg_finditer(pattern,subject,flags=0):
    try:
        p =re.compile(pattern,flags)
        return p.finditer(subject)
    except Exception as e:
        print_red('[ERROR]:%s  [REGEX]:%s'%(e, pattern))
        print()
        return ()

def print_blue(s_str):
    print(Fore.BLUE + str(s_str))

def print_red(s_str):
    print(Fore.RED + str(s_str))

def print_green(s_str):
    print(Fore.GREEN + str(s_str))

def print_bg_blue(s_str):
    print(Back.BLUE + str(s_str))

def print_bg_red(s_str):
    print(Back.RED + str(s_str))

def print_bg_green(s_str):
    print(Back.GREEN +str(s_str))



if __name__ == '__main__':
    a='abcde afgh ijkalmno pqrastuvwxyz'
    print(reg_replace(r'a','',a))
    print(reg_replacenum(r'a','',a))
    print(reg_match(r'a.*?$',a))
    print(reg_fullmatch(r'b[cd].*',a,1,3))
    print(reg_search(r'b.*?',a))
    print(reg_split(r'a',a))
    print(reg_findall(r'a.*?',a))
    print(reg_finditer(r'a.*?',a))

    print_red('asdfasdf');
    print_bg_red('asdfasdf');
    print_green('asdfasdf');
    print_bg_green('asdfasdf');
    input('按任意键继续...')
