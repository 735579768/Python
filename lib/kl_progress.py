import threading,sys
import time
class kl_progress(threading.Thread): #The timer class is derived from the class threading.Thread
    def __init__(self, text='', interval=0.5):
        threading.Thread.__init__(self)
        self.text = text
        self.cur_text = text+'   '
        self.interval = interval
        self.text_show = False
        self.thread_stop=False

    def show(self):
        self.text_show=True

    def hide(self):
        self.text_show=False

    def run(self): #Overwrite run() method, put what you want the thread do here
        while True:
            if self.cur_text==self.text+'   ':
                self.cur_text=self.text+'.  '
            elif self.cur_text==self.text+'.  ':
                self.cur_text=self.text+'.. '
            elif self.cur_text==self.text+'.. ':
                self.cur_text=self.text+'...'
            elif self.cur_text==self.text+'...':
                self.cur_text=self.text+'   '

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
    progress.show()
    progress.join()
    input('按任意键继续...')
