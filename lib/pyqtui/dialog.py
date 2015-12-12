from PyQt5.QtWidgets import *
class Dialog(QDialog):
    def __init__(self,parent = None):
       QDialog .__init__(self,parent)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    dlg = Dialog()
    dlg.resize(400, 300)
    dlg.setWindowTitle("自定义编辑框测试")
    #dlg.setWindowFlags()
    dlg.setWindowOpacity(0.9)
    dlg.show()
    dlg.exec_()
    app.exit()
