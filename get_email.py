import poplib
from email import parser
from email.header import decode_header
from email.utils import parseaddr
poplib._MAXLINE=20480
#解码subject和email的编码
def decode_str(s):
  value, charset = decode_header(s)[0]
  if charset:
    value = value.decode(charset)
  return value
'''
Message对象本身可能是一个MIMEMultipart对象，即包含嵌套的其他MIMEBase对象，嵌套可能还不止一层。
所以我们要递归地打印出Message对象的层次结构：
'''
# indent用于缩进显示:
def print_info(msg, indent=0):
  restr=''
  if indent == 0:
    # 邮件的From, To, Subject存在于根对象上:
    for header in ['From', 'To', 'Subject']:
      value = msg.get(header, '')
      if value:
        if header=='Subject':
          # 需要解码Subject字符串:
          value = decode_str(value)
        else:
          # 需要解码Email地址:
          hdr, addr = parseaddr(value)
          name = decode_str(hdr)
          value = u'%s <%s>' % (name, addr)
      print('%s%s: %s' % (' ' * indent, header, value))
      restr+='%s%s: %s' % (' ' * indent, header, value)
  if (msg.is_multipart()):
    # 如果邮件对象是一个MIMEMultipart,
    # get_payload()返回list，包含所有的子对象:
    parts = msg.get_payload()
    for n, part in enumerate(parts):
      print('%spart %s' % (' ' * indent, n))
      print('%s--------------------' % (' ' * indent))
      # 递归打印每一个子对象:
      print_info(part, indent + 1)
  else:
    # 邮件对象不是一个MIMEMultipart,
    # 就根据content_type判断:
    content_type = msg.get_content_type()
    if content_type=='text/plain' or content_type=='text/html':
      # 纯文本或HTML内容:
      content = msg.get_payload(decode=True)
      # 要检测文本编码:
      charset = guess_charset(msg)
      if charset:
            content = content.decode(charset)
      else:
            content = content.decode()
      print('%sText: %s' % (' ' * indent, content + '...'))
    else:
      # 不是文本,作为附件处理:
      print('%sAttachment: %s' % (' ' * indent, content_type))
def guess_charset(msg):
  # 先从msg对象获取编码:
  charset = msg.get_charset()
  if charset is None:
    # 如果获取不到，再从Content-Type字段获取:
    content_type = msg.get('Content-Type', '').lower()
    pos = content_type.find('charset=')
    if pos >= 0:
      charset = content_type[pos + 8:].strip()
  return charset
host = 'pop.qq.com'
username = '735579768@qq.com'
password = 'zkl735579768'

# 连接到POP3服务器:
pop_conn = poplib.POP3_SSL(host)
# 可选:打印POP3服务器的欢迎文字:
print(pop_conn.getwelcome())
# 身份认证:
pop_conn.user(username)
pop_conn.pass_(password)

# 获取服务器上信件信息，返回是一个列表，第一项是一共有多上封邮件，第二项是共有多少字节
ret=pop_conn.stat()
print('Messages: %s. Size: %s' %ret )

#要查找的邮件索引
emailindex=0

# 需要取出所有信件的头部，解析出发件人是谁,信件id是从1开始的。
for i in range(1, ret[0]+1):
    print('正在查询第%d条邮件信息...'%(i))
    # 取出信件头部。注意：top指定的行数是以信件头为基数的，也就是说当取0行，
    # 其实是返回头部信息，取1行其实是返回头部信息之外再多1行。,mlist[0]是状态 mlist[1]是信件头的内容
    mlist = pop_conn.top(i, 0)
    #解析成email object
    msgcon=b"\r\n".join(mlist[1]).decode()
    msgheader =parser.Parser().parsestr(msgcon)
    #取发件人是谁
    addrfrom = str(msgheader.get('from'))
    #邮件主题
    subject = decode_str(str(msgheader.get('subject')))
    #接收方邮箱
    toemail = decode_str(str(msgheader.get('to')))
    if addrfrom.find('service@ainiku.com')!=-1:
        emailindex=i
        print("找到邮件啦，索引为%d,发件主题为%s"%(i, subject))


# 列出服务器上邮件信息，这个会对每一封邮件都输出id和大小。不象stat输出的是总的统计信息
#ret = pop_conn.list()
#print (ret)
if emailindex==0:
    print('没有找到相关邮件!')
# 取查找到的邮件完整信息，在返回值里，是按行存储在down[1]的列表里的。down[0]是返回的状态信息
down = pop_conn.retr(emailindex)
msg_content = b"\r\n".join(down[1]).decode()
#解析邮件到email object:
message =parser.Parser().parsestr(msg_content)
print(message)

# 可以根据邮件索引号直接从服务器删除邮件:
# pop_conn.dele(index)

addrfrom = decode_str(str(message.get('from')))
    #邮件主题
subject = decode_str(str(message.get('subject')))
body = print_info(message)
print("%s,%s"%(addrfrom, subject))
#过滤出想要的发件人信息
pop_conn.quit()
