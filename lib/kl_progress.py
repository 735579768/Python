import threading,sys,time
class kl_progress(threading.Thread): #The timer class is derived from the class threading.Thread
    def __init__(self, text='', interval=0.2,total_len=6):
        threading.Thread.__init__(self)
        self.text = text
        self.cur_text = text+'   '
        self.interval = interval
        self.text_show = True
        self.thread_stop=False
        self.total_len=total_len
        self.cur_len=0

    def show(self):
        self.text_show=True

    def hide(self):
        self.text_show=False

    def setwidth(self,w=6):
        self.total_len=w

    def settext(self,text):
        self.text=text

    def run(self): #Overwrite run() method, put what you want the thread do here
        while True:
            self.cur_text=self.text
            for i in range(0,self.cur_len):
                self.cur_text+='.'
            for i in range(0,self.total_len-self.cur_len):
                self.cur_text+=' '

            if self.cur_len==self.total_len:
                self.cur_len=0

            self.cur_len+=1

            if self.text_show:
                sys.stdout.write(self.cur_text+'\r')
                sys.stdout.flush()

            if self.thread_stop:
                break

            time.sleep(self.interval)
    def stop(self):
        self.thread_stop = True

if __name__ == '__main__':
    progress=kl_progress('正在运行中')
    progress.start()
    progress.join()
    input('按任意键继续...')
