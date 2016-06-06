# -*- coding: utf-8 -*-
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
        self.resize(500,300);
        self.btn1=QPushButton('添加数据')
        self.btn2=QPushButton('删除数据')
        self.model=QStandardItemModel(4,4);
        self.model.setHorizontalHeaderLabels(['标题1','标题2','标题3','标题4'])
        for row in range(4):
            for column in range(4):
                item = QStandardItem("row %s, column %s"%(row,column))
                self.model.setItem(row, column, item)

        self.tableView=QTableView();
        self.tableView.setModel(self.model)
        #下面代码让表格100填满窗口
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        dlgLayout=QVBoxLayout();
        dlgLayout.addWidget(self.tableView)
        dlgLayout.addWidget(self.btn1)
        dlgLayout.addWidget(self.btn2)
        self.setLayout(dlgLayout)
        self.btn1.clicked.connect(self.adddata)
        self.btn2.clicked.connect(self.deldata)

    def adddata(self):
        self.model.appendRow([
            QStandardItem("row %s, column %s"%(11,11)),
            QStandardItem("row %s, column %s"%(11,11)),
            QStandardItem("row %s, column %s"%(11,11)),
            QStandardItem("row %s, column %s"%(11,11)),
            ])
    def deldata(self):
        # indexs=self.tableView.selectionModel().selection().indexes()
        # if len(indexs)>0:
        #     index = indexs[0]
        #     self.model.removeRows(index.row(),1)
        #删除第一行
        index=self.tableView.currentIndex()
        print(index.data())
        self.model.removeRow(index.row())
app = QApplication(sys.argv)
#全局设置QPushButton的背景样式
dlg = myDialog()
dlg.show()
dlg.exec_()
app.exit()

