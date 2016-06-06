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

        conLayout = QVBoxLayout()
        self.lv = QListWidget()
        #排序
        self.lv.setSortingEnabled(1)
        item = ['OaK','Banana','Apple','Orange','Grapes','Jayesh']

        #创建列表项
        listItem = []
        for lst in item:
            listItem.append(QListWidgetItem(QIcon("images/qt.jpg"),self.tr(lst)))

        #把列表项添加到listwidget中
        for i in range(len(listItem)):
            self.lv.insertItem(i+1,listItem[i])

        conLayout.addWidget(self.lv)
        self.setLayout(conLayout)
        self.lv.itemClicked.connect(self.clickitem)


    def clickitem(self,obj):
        print(obj.text())
        self.__msg(obj.text())

    def __msg(self,s):
        box=QMessageBox()
        box.setText(s)
        box.setWindowTitle(self.tr('信息提醒'))
        box.addButton(self.tr("确定"), QMessageBox.ActionRole);
        box.exec()

app = QApplication(sys.argv)
dlg = myDialog()
dlg.show()
dlg.exec_()
app.exit()
