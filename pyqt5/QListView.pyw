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
        #model=QStringListModel()
        model=QStandardItemModel(6,6);


        for row in range(6):
            for column in range(6):
                item = QStandardItem("row %s, column %s"%(row,column))
                model.setItem(row, column, item)

        listView=QListView();
        listView.setModel(model)

        dlgLayout=QVBoxLayout();
        dlgLayout.addWidget(listView)
        self.setLayout(dlgLayout)

app = QApplication(sys.argv)
#全局设置QPushButton的背景样式
dlg = myDialog()
dlg.show()
dlg.exec_()
app.exit()

'''
通过实现 itemClicked (QTableWidgetItem *) 信号的槽函数，就可以获得鼠标单击到的单元格指针，进而获得其中的文字信息
connect(tableWidget,SIGNAL(itemDoubleClicked(QTreeWidgetItem*,int)),this,SLOT(getItem(QTreeWidgetItem*,int)));
//将itemClicked信号与函数getItem绑定
'''
