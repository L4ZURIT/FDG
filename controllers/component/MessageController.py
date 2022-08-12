from PyQt5.uic import *
from PyQt5.QtWidgets import *
import sys



class Messenger():

    @staticmethod
    def ask(what:str) -> bool:

        ans = QMessageBox.question(None, "FDG", what)
        


        return True



class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)


        Messenger.ask("ЧТО?")


        #loadUi('untitled.ui',self)
        #self.setCentralWidget(QPushButton('BEGIN'))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())