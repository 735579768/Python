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
        self.urlLineEdit = QLineEdit()
        self.combox=QComboBox()
        self.htmlEdit = QTextEdit()
        self.okBtn = QPushButton("取网页")
        self.combox.addItem('GET')
        self.combox.addItem('POST')
        self.paramEdit=QTextEdit()
        peditLayout = QHBoxLayout()
        peditLayout.addWidget(self.paramEdit)

        gridLayout = QGridLayout()
        gridLayout.addWidget(usr, 0, 0, 1, 1)
        gridLayout.addWidget(self.urlLineEdit, 0, 1, 1, 4);
        gridLayout.addWidget(self.combox, 0, 5, 1, 1);
        gridLayout.addWidget(self.okBtn, 0, 6, 1, 2);
        # gridLayout.addWidget(self.paramEdit, 1, 0, 1, 8);



        editLayout = QVBoxLayout()
        editLayout.addWidget(self.htmlEdit);

        dlgLayout = QVBoxLayout()
        dlgLayout.setContentsMargins(10, 10, 10, 10)
        dlgLayout.addLayout(gridLayout)
        dlgLayout.addLayout(peditLayout)
        dlgLayout.addLayout(editLayout)
        #dlgLayout.addStretch(40)

        self.setLayout(dlgLayout)
        self.okBtn.clicked.connect(self.accept)
        self.setWindowTitle("取网页内容")
        self.resize(400, 300)

    def accept(self):
        try:
            ht=kl_http.kl_http()
            strr=self.urlLineEdit.text()
            metch=self.combox.currentText()
            if not strr:
                strr='http://www.baidu.com/'
            r=None
            if metch=='GET':
                r=ht.geturl(strr)
            else:
                r=ht.posturl(strr)

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