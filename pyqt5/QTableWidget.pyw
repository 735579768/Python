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
        self.resize(500,300);
        btn1=QPushButton('添加')
        btn2=QPushButton('清空')

        conLayout = QHBoxLayout()
        tableWidget=QTableWidget()
        tableWidget.setRowCount(5)
        tableWidget.setColumnCount(4)
        conLayout.addWidget(tableWidget)
        for i in range(5):
            for j in range(4):
                tableWidget.setItem(i,j, QTableWidgetItem(QIcon("images/qt.jpg"),self.tr(str(i)+str(j))))
        self.setLayout(conLayout)

    def clearComboBox(self):
        #清空组合框
        self.sexComboBox.clear()

    def additem(self):
        #添加文本
        self.sexComboBox.addItem('测试数据')

    def comboxchange(self):
        QMessageBox.warning(self,"警告",str(self.sexComboBox.currentIndex())+self.tr(':')+self.sexComboBox.currentText(),QMessageBox.Yes)

app = QApplication(sys.argv)

#全局设置QPushButton的背景样式
dlg = myDialog()
dlg.show()
dlg.exec_()
app.exit()
