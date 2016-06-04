import threading,sys,time,os

class kl_progressbar(object): #The timer class is derived from the class threading.Thread
    def __init__(self, text='',total_len=10):
        threading.Thread.__init__(self)
        self.text = text
        self.cur_text = text
        self.total_len=total_len
        self.cur_len=0
        #上一次字符串的长度
        self.prev_text_len=0

    def __cleartext(self):
        cleartext=''
        cd=self.total_len+len(bytes(self.text, encoding = "utf8"))
        for i in range(0,cd):
            cleartext+=' '
        sys.stdout.write(cleartext+'\r')
        sys.stdout.flush()

    def setwidth(self,w=6):
        self.total_len=w

    def settext(self,text):
        self.text=text

    def show(self): #Overwrite run() method, put what you want the thread do here
        self.cur_text=self.text
        for i in range(0,self.cur_len):
            self.cur_text+='.'

        tem_len=self.prev_text_len-len(bytes(self.cur_text,encoding='utf8'))
        if tem_len>0:
            for i in range(0,tem_len):
                self.cur_text+=' '

        if self.cur_len==self.total_len:
            self.cur_len=0
        else:
            self.cur_len+=1

        self.prev_text_len=len(bytes(self.cur_text,encoding='utf8'))
        sys.stdout.write(self.cur_text+'\r')
        sys.stdout.flush()

if __name__ == '__main__':
    progress=kl_progressbar('正在运行中')

    while 1:
        time.sleep(.2)
        progress.show()
    os.system("pause")
