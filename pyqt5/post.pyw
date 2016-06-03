#!/usr/bin/python3
#coding:utf-8

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys,kl_http

class LoginDlg(QDialog):
    def __init__(self, parent=None):
        super(LoginDlg, self).__init__(parent)
        self.setWindowFlags(Qt.WindowMaximizeButtonHint|Qt.WindowMinimizeButtonHint|Qt.WindowCloseButtonHint)

        usr = QLabel("地址：")
        pwd = QLabel("内容：")
        #控件
        self.urlLineEdit = QLineEdit()
        self.combox=QComboBox()
        self.htmlEdit = QTextEdit()
        self.paramEdit=QTextEdit()
        self.headEdit=QTextEdit()
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
        hGroupbox.setFixedHeight(80)
        pGroupbox.setFixedHeight(80)


        gridLayout = QGridLayout()
        gridLayout.addWidget(usr, 0, 0, 1, 1)
        gridLayout.addWidget(self.urlLineEdit, 0, 1, 1, 4);
        gridLayout.addWidget(self.combox, 0, 5, 1, 1);
        gridLayout.addWidget(self.okBtn, 0, 6, 1, 2);


        dlgLayout = QVBoxLayout()
        dlgLayout.setContentsMargins(10, 10, 10, 10)
        dlgLayout.addLayout(gridLayout)
        dlgLayout.addWidget(hGroupbox)
        dlgLayout.addWidget(pGroupbox)
        dlgLayout.addWidget(cGroupbox)
        #dlgLayout.addStretch(40)

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
            if not header:
                ht.setheaders(header)
            if not strr:
                strr='http://www.baidu.com/'
            r=None
            if metch=='GET':
                r=ht.geturl(strr,param)
            else:
                r=ht.posturl(strr,param)

            if r:
                self.htmlEdit.setPlainText(r.read().decode())
        except Exception as e:
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