import threading,sys,time,os
def get_console_width():
    """Return width of available window area. Autodetection works for
       Windows and POSIX platforms. Returns 80 for others

       Code from http://bitbucket.org/techtonik/python-pager
    """

    if os.name == 'nt':
        STD_INPUT_HANDLE  = -10
        STD_OUTPUT_HANDLE = -11
        STD_ERROR_HANDLE  = -12

        # get console handle
        from ctypes import windll, Structure, byref
        try:
            from ctypes.wintypes import SHORT, WORD, DWORD
        except ImportError:
            # workaround for missing types in Python 2.5
            from ctypes import (
                c_short as SHORT, c_ushort as WORD, c_ulong as DWORD)
        console_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

        # CONSOLE_SCREEN_BUFFER_INFO Structure
        class COORD(Structure):
            _fields_ = [("X", SHORT), ("Y", SHORT)]

        class SMALL_RECT(Structure):
            _fields_ = [("Left", SHORT), ("Top", SHORT),
                        ("Right", SHORT), ("Bottom", SHORT)]

        class CONSOLE_SCREEN_BUFFER_INFO(Structure):
            _fields_ = [("dwSize", COORD),
                        ("dwCursorPosition", COORD),
                        ("wAttributes", WORD),
                        ("srWindow", SMALL_RECT),
                        ("dwMaximumWindowSize", DWORD)]

        sbi = CONSOLE_SCREEN_BUFFER_INFO()
        ret = windll.kernel32.GetConsoleScreenBufferInfo(
                console_handle, byref(sbi))
        if ret == 0:
            return 0
        return sbi.srWindow.Right+1

    elif os.name == 'posix':
        from fcntl import ioctl
        from termios import TIOCGWINSZ
        from array import array

        winsize = array("H", [0] * 4)
        try:
            ioctl(sys.stdout.fileno(), TIOCGWINSZ, winsize)
        except IOError:
            pass
        return (winsize[1], winsize[0])[0]

    return 80


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
    print(get_console_width())
    progress=kl_progressbar('正在运行中')

    while 1:
        time.sleep(.2)
        progress.show()
    os.system("pause")
