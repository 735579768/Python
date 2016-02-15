import threading,sys,time
class kl_progress(threading.Thread): #The timer class is derived from the class threading.Thread
    def __init__(self, text='', interval=0.2,total_len=6):
        threading.Thread.__init__(self)
        self.text = text
        self.cur_text = text
        self.interval = interval
        self.text_show = True
        self.thread_stop=False
        self.total_len=total_len
        self.cur_len=0
        #上一次字符串的长度
        self.prev_text_len=0
    def __cleartext(self):
        time.sleep(self.interval*2)
        cleartext=''
        cd=self.total_len+len(bytes(self.text, encoding = "utf8"))
        for i in range(0,cd):
            cleartext+=' '
        sys.stdout.write(cleartext+'\r')
        sys.stdout.flush()

    def show(self):
        self.text_show=True

    def hide(self):
        self.text_show=False
        self.__cleartext()

    def setwidth(self,w=6):
        self.total_len=w

    def settext(self,text):
        self.text=text

    def stop(self):
        self.thread_stop = True
        self.__cleartext()

    def run(self): #Overwrite run() method, put what you want the thread do here
        while True:
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
            if self.text_show:
                sys.stdout.write(self.cur_text+'\r')
                sys.stdout.flush()

            if self.thread_stop:
                break

            time.sleep(self.interval)


if __name__ == '__main__':
    progress=kl_progress('正在运行中')
    progress.start()

    scd=1
    te='走'
    while True:
        if scd==9:
            te='走'
            scd=0
        else:
            te+='走'
        progress.settext(te)
        scd+=1
        time.sleep(1)
    progress.join()
    input('按任意键继续...')
