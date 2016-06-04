#!/usr/bin/python3
#coding:utf-8

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys,kl_http,chardet

class LoginDlg(QDialog):
    def __init__(self, parent=None):
        super(LoginDlg, self).__init__(parent)
        self.setWindowFlags(Qt.WindowMaximizeButtonHint|Qt.WindowMinimizeButtonHint|Qt.WindowCloseButtonHint)

        addr = QLabel("地址：")
        #控件
        self.urlLineEdit = QLineEdit()
        self.combox=QComboBox()
        self.htmlEdit = QPlainTextEdit()
        self.paramEdit=QPlainTextEdit()
        self.headEdit=QPlainTextEdit()
        self.okBtn = QPushButton("取网页")
        self.combox.addItem('GET')
        self.combox.addItem('POST')

        #分组
        hGroupbox=QGroupBox('请求头(以换行为分隔)')
        pGroupbox=QGroupBox('请求参数(以换行或&&分隔)')
        cGroupbox=QGroupBox('响应内容')
        heditLayout = QHBoxLayout()
        peditLayout = QHBoxLayout()
        ceditLayout = QVBoxLayout()

        heditLayout.addWidget(self.headEdit)
        peditLayout.addWidget(self.paramEdit)
        ceditLayout.addWidget(self.htmlEdit)
        hGroupbox.setLayout(heditLayout)
        pGroupbox.setLayout(peditLayout)
        cGroupbox.setLayout(ceditLayout)

        self.combox.setFixedWidth(50)
        self.okBtn.setMaximumWidth(200)
        #hGroupbox.setFixedHeight(80)
        #pGroupbox.setFixedHeight(80)


        searchLayout = QHBoxLayout()
        searchLayout.addWidget(addr)
        searchLayout.addWidget(self.urlLineEdit)
        searchLayout.addWidget(self.combox)
        searchLayout.addWidget(self.okBtn)


        dlgLayout = QVBoxLayout()
        dlgLayout.setContentsMargins(10, 10, 10, 10)
        dlgLayout.addLayout(searchLayout)
        dlgLayout.setStretchFactor(searchLayout,1)
        dlgLayout.addWidget(hGroupbox)
        dlgLayout.setStretchFactor(hGroupbox,1)
        dlgLayout.addWidget(pGroupbox)
        dlgLayout.setStretchFactor(pGroupbox,1)
        dlgLayout.addWidget(cGroupbox)
        dlgLayout.setStretchFactor(cGroupbox,5)

        #默认值
        self.urlLineEdit.setText('http://user.zhaokeli.com')
        self.setLayout(dlgLayout)
        self.okBtn.clicked.connect(self.accept)
        self.setWindowTitle("取网页内容")
        self.resize(800,600)

    def accept(self):
        try:
            ht=kl_http.kl_http()
            strr=self.urlLineEdit.text()
            metch=self.combox.currentText()
            param=self.paramEdit.toPlainText()
            header=self.headEdit.toPlainText()
            if header:
                ht.setheaders(header)
            if not strr:
                strr='http://www.baidu.com/'
            r=None
            if metch=='GET':
                r=ht.geturl(strr,param)
            else:
                r=ht.posturl(strr,param)

            if r:
                rr=r.read()
                charset=chardet.detect(rr)
                self.htmlEdit.setPlainText(rr.decode(charset['encoding']))
        except Exception as e:
            self.htmlEdit.setPlainText('%s'%e)
            print(e)

app = QApplication(sys.argv)
app.setStyleSheet('''
    QTextEdit{width:100%;height:100%;}
    QDialog{border:solid 1px #cccccc;}
    ''')
dlg = LoginDlg()
dlg.show()
dlg.exec_()
app.exit()