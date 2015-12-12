from PyQt5.QtWidgets import *
class Button(QPushButton):
    def __init__(self, text='',parent = None):
       QPushButton .__init__(self,text)
    def getText(self):
        return self.text().strip()
    def setClick(self,callback):
        self.clicked.connect(callback)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    dlg = QDialog()
    dlg.resize(400, 300)
    dlg.setWindowTitle("自定义按钮测试")
    #定义按钮
    okbtn=Button('确定')
    modbtn=Button('增加')
    okbtn.setClick(lambda:QMessageBox.warning(dlg,'警告','单击事件',QMessageBox.Yes))
    modbtn.setClick(lambda:QMessageBox.warning(dlg,'警告','单击事件',QMessageBox.Yes))
    dlgLayout = QVBoxLayout()
    dlgLayout.setContentsMargins(40, 40, 40, 40)
    dlgLayout.addWidget(okbtn)
    dlgLayout.addWidget(modbtn)
    dlgLayout.addStretch(40)
    dlg.setLayout(dlgLayout)
    
    dlg.show()
    dlg.exec_()
    app.exit()
