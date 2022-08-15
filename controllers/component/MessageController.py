from PyQt5.uic import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import sys


# Инструмент для открытия диалоговых окон и прочих всплывающих сообщений
class Messenger():

    @staticmethod
    def ask_y_n(what:str) -> bool:
        dial = QDialog(None, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        dial.setWindowTitle("FDG")
        dial.setFixedSize(300, 150)
        dial_layout = QVBoxLayout()
        lbl = QLabel(what)
        lbl.setWordWrap(True)
        lo_btns = QHBoxLayout()
        lo_btns.addSpacerItem(QSpacerItem(100, 1)) # Расстояние до кнопок
        btn_y = QPushButton("Да")
        btn_y.clicked.connect(dial.accept)
        btn_n = QPushButton("Нет")
        btn_n.clicked.connect(dial.reject)
        lo_btns.addWidget(btn_n)
        lo_btns.addWidget(btn_y)
        dial_layout.addWidget(lbl)
        dial_layout.addLayout(lo_btns)
        dial.setLayout(dial_layout)     
        return bool(dial.exec())

    @staticmethod
    def err(what:str):
        ms = QMessageBox.critical(None, "FDG", what)

    @staticmethod
    def say(what:str):
        ms = QMessageBox.information(None, "FDG", what)

    @staticmethod
    def find_file(what:str, filetypes:list) -> str:
        file , check = QFileDialog.getOpenFileName(None, what,"", ";;".join(filetypes))
        if check:
            return file

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)


        print(Messenger.ask_y_n("ЧТО?"))


        #loadUi('untitled.ui',self)
        #self.setCentralWidget(QPushButton('BEGIN'))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())