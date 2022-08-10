from PyQt5.uic import *
from PyQt5.QtWidgets import *
import sys



class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('views/main_window.ui',self)
        



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())