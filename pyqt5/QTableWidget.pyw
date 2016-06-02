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
        # strlist=['a','b','a','b']
        # tableWidget.setHorizontalHeaderLabels(strlist)
        tableWidget.setHorizontalHeaderItem(1,QTableWidgetItem('你好'))
        #默认表格是可编辑的,下面设置为只读
        tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers);
        #整行选中的方式
        tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows);
        #隐藏列表头
        #tableWidget.verticalHeader().setVisible(False);
        #隐藏行表头
        #tableWidget.horizontalHeader().setVisible(False);
        #还可以将行和列的大小设为与内容相匹配
        tableWidget.resizeColumnsToContents();
        tableWidget.resizeRowsToContents();

        tableWidget.setRowCount(5)
        tableWidget.setColumnCount(4)
        conLayout.addWidget(tableWidget)
        for i in range(5):
            for j in range(4):
                tableWidget.setItem(i,j, QTableWidgetItem(QIcon("images/qt.jpg"),self.tr(str(i)+str(j))))
                #可以在单元格中加入控件
                # comBox = QComboBox();
                # comBox.addItem("Y");
                # comBox.addItem("N");
                # tableWidget.setCellWidget(i,j,comBox);

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

'''
通过实现 itemClicked (QTableWidgetItem *) 信号的槽函数，就可以获得鼠标单击到的单元格指针，进而获得其中的文字信息
connect(tableWidget,SIGNAL(itemDoubleClicked(QTreeWidgetItem*,int)),this,SLOT(getItem(QTreeWidgetItem*,int)));
//将itemClicked信号与函数getItem绑定
'''
