# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Python\pyqt5\my.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!
import sys
import my
from PyQt5 import QtCore, QtGui, QtWidgets

if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    dlg=QtWidgets.QWidget()
    ui=my.Ui_Dialog()
    ui.setupUi(dlg)
    dlg.show()
    sys.exit(app.exec_())

    #dlg.exec_()
    #app.exit()

