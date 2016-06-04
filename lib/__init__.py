from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
import smtplib,os
class kl_smtp:
    def __init__(self,mail_host,mail_user,mail_pass,mail_postfix):
        self.mail_host=mail_host
        self.mail_user=mail_user
        self.mail_pass=mail_pass
        self.mail_postfix=mail_postfix

    def sendmail(self,to_list,sub,content,attachpath=''):
        '''''
        to_list:发给谁
        sub:主题
        content:内容
        attachpath:附件路径
        send_mail("aaa@126.com","sub","content")
       '''
        me=self.mail_user+"<"+self.mail_user+"@"+self.mail_postfix+">"
        msg = MIMEMultipart()
        msg['Subject'] = sub
        msg.attach(MIMEText(content, 'plain', 'utf-8'))
        msg['From'] = me
        msg['To'] = ";".join(to_list)
        #添加附件
        if attachpath != '' :
            basename = os.path.basename(attachpath)
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(attachpath,'rb').read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="'+basename+'"')
            msg.attach(part)
        try:
            s = smtplib.SMTP()
            s.connect(self.mail_host)
            s.login(self.mail_user,self.mail_pass)
            s.sendmail(me, to_list, msg.as_string())
            s.close()
            return True
        except Exception as e:
            print (str(e))
            return False

if __name__ == '__main__':
    mailto_list=["735579768@qq.com","735579768@qq.com"]
    stp=kl_smtp(mail_host='ainiku.com',mail_user='service',mail_pass='adminrootkl',mail_postfix='ainiku.com')
    if stp.sendmail(mailto_list,"这个是邮件主题","这里是邮件内容",'kl_reg.py'):
        print ("发送成功")
    else:
        print ("发送失败")
