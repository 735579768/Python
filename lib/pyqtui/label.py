from PyQt5.QtWidgets import *
class Label(QLabel):
    def __init__(self,parent = None):
       QLabel .__init__(self,parent)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    dlg = QDialog()
    dlg.resize(400, 300)
    dlg.setWindowTitle("自定义编辑框测试")
    
    #定义按钮
    ed=Label('这是一个标签')
    dlgLayout = QVBoxLayout()
    dlgLayout.setContentsMargins(40, 40, 40, 40)
    dlgLayout.addWidget(ed)
    dlgLayout.addStretch(40)
    dlg.setLayout(dlgLayout)
    
    dlg.show()
    dlg.exec_()
    app.exit()