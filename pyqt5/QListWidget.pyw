# -*- coding: utf-8 -*-
"""第一个程序"""
#from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

class myDialog(QDialog):
    """docstring for myDialog"""
    def __init__(self, arg=None):
        super(myDialog, self).__init__(arg)
        self.setWindowTitle("first window")
        self.resize(400,300);



        conLayout = QVBoxLayout()

        self.lv = QListWidget()
        #排序
        self.lv.setSortingEnabled(1)
        item = ['OaK','Banana','Apple','Orange','Grapes','Jayesh']

        listItem = []
        for lst in item:
            listItem.append(QListWidgetItem(QIcon("images/qt.jpg"),self.tr(lst)))

        for i in range(len(listItem)):
            self.lv.insertItem(i+1,listItem[i])

        conLayout.addWidget(self.lv)
        self.setLayout(conLayout)



    def okfunc(self):
        self.cancelBtn.setText('取消按钮改变啦')
        QMessageBox.warning(self,"警告","信息提示！",QMessageBox.Yes)

app = QApplication(sys.argv)
dlg = myDialog()
dlg.show()
dlg.exec_()
app.exit()
