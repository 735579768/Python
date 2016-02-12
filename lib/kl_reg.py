import re
A=re.A
DEBUG=re.DEBUG
I=re.I
L=re.L
M=re.M
S=re.S
X=re.X
def replace(pattern,replacement,subject,flags=0):
    p = re.compile(pattern,flags)
    return p.sub(replacement,subject)

def replacenum(pattern,replacement,subject,flags=0):
    p = re.compile(pattern,flags)
    return p.subn(replacement,subject)

#从字符串中查找匹配,匹配失败返回None,成功默认返回第一个匹配,如果想完全匹配请在正则上加上$，这时就跟fullmatch一样
def match(pattern,subject,pos=0,endpos=0,flags=0):
    endpos =len(subject)
    p = re.compile(pattern,flags)
    return p.match(subject)

#匹配整个字符串,匹配失败返回None
def fullmatch(pattern,subject,pos=0,endpos=0,flags=0):
    endpos =len(subject)
    p = re.compile(pattern,flags)
    return p.fullmatch(subject,pos,endpos)

#搜索失败返回None,成功返回一个match对象,可以使用match.group([num])取分组信息
def search(pattern,subject,pos=0,endpos=0,flags=0):
    endpos=len(subject)
    p = re.compile(pattern,flags)
    return p.search(subject,pos,endpos)

#按照能够匹配的子串将subject分割后返回列表。
def split(pattern,subject,flags=0):
    p = re.compile(pattern,flags)
    return p.split(subject)

#搜索string，以列表形式返回全部能匹配的子串。
def findall(pattern,subject,flags=0):
    p =re.compile(pattern,flags)
    return p.findall(subject)

#搜索string，返回一个顺序访问每一个匹配结果（Match对象）的迭代器。
def finditer(pattern,subject,flags=0):
    p =re.compile(pattern,flags)
    return p.findall(subject)

if __name__ == '__main__':
    a='abcde afgh ijkalmno pqrastuvwxyz'
    print(replace(r'a','',a))
    print(replacenum(r'a','',a))
    print(match(r'a.*?$',a))
    print(fullmatch(r'b[cd].*',a,1,3))
    print(search(r'b.*?',a))
    print(split(r'a',a))
    print(findall(r'a.*?',a))
    print(finditer(r'a.*?',a))
    input('按任意键继续...')
