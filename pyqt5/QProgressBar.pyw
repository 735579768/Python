# -*- coding: utf-8 -*-
"""第一个程序"""
#from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

class myDialog(QDialog):
    """docstring for myDialog"""
    def __init__(self, arg=None):
        super(myDialog, self).__init__(arg)
        self.setWindowTitle("first window")
        self.setWindowFlags(Qt.WindowMaximizeButtonHint|Qt.WindowMinimizeButtonHint|Qt.WindowCloseButtonHint)
        self.resize(400,300);
        btn1=QPushButton(self.tr('进度'))
        btn2=QPushButton(self.tr('重置'))
        btn1.clicked.connect(self.clickitem1)
        btn2.clicked.connect(self.clickitem2)


        conLayout = QVBoxLayout()
        # self.lv = QListWidget()
        self.probar=QProgressBar()
        self.probar.setMaximum(100)

        conLayout.addWidget(self.probar)
        conLayout.addWidget(btn1)
        conLayout.addWidget(btn2)
        self.setLayout(conLayout)

    def clickitem1(self,obj):
        for i in range(101):
            self.probar.setValue(i);

    def clickitem2(self,obj):
        self.probar.reset();


app = QApplication(sys.argv)
dlg = myDialog()
dlg.show()
dlg.exec_()
app.exit()
