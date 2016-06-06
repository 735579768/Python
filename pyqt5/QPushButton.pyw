# -*- coding: utf-8 -*-
"""第一个程序"""
#from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor
from PyQt5.QtCore import *
import sys

class myDialog(QDialog):
    """docstring for myDialog"""
    def __init__(self, arg=None):
        super(myDialog, self).__init__(arg)
        self.setWindowTitle("first window")
        self.setWindowFlags(Qt.WindowMaximizeButtonHint|Qt.WindowMinimizeButtonHint|Qt.WindowCloseButtonHint)
        self.resize(400,300);

        #添加两个按钮

        self.okBtn = QPushButton("确定")
        self.cancelBtn = QPushButton("取消")
        btn1 = QPushButton("btn1")
        btn2 = QPushButton("btn2")

        #单独设置ok按钮样式
        self.okBtn.setStyleSheet('''color: white;
                        background-color: yellow;
                        selection-color: yellow;
                        selection-background-color: blue''')

        #应用名字为cancel的样式
        self.cancelBtn.setObjectName('cancel')

        btnLayout = QHBoxLayout()
        btnLayout.addWidget(self.okBtn)
        btnLayout.addWidget(self.cancelBtn)
        btnLayout.addWidget(btn1)
        btnLayout.addWidget(btn2)
        self.setLayout(btnLayout)

        #注册信号槽
        self.okBtn.clicked.connect(self.okfunc)

    def okfunc(self):
        self.cancelBtn.setText('取消按钮改变啦')
        QMessageBox.warning(self,"警告","信息提示！",QMessageBox.Yes)

app = QApplication(sys.argv)

#全局设置QPushButton的背景样式
app.setStyleSheet('''
    QPushButton{
        background-color: #0f0 ;
        height:30px;
        border-style: outset;
        border-width: 2px;
        border-radius: 10px;
        border-color: beige;
        font: bold 14px;
        min-width: 10em;
        padding: 6px;
    }
    QPushButton:hover {
    background-color: yellow;
    border-style: inset;
    }
    QPushButton:pressed {
    background-color: rgb(224, 0, 0);
    border-style: inset;
    }
    QPushButton#cancel{
        background-color: red ;
    }

    ''')
dlg = myDialog()
dlg.show()
dlg.exec_()
app.exit()
