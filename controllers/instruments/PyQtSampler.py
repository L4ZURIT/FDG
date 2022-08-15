from pprint import pprint
from PyQt5.uic import *
from PyQt5.QtWidgets import *
import sys



class EditableTable(QTableWidget):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)

    # Заполняет таблицу полученными данными
    def set_content(self, content:dict):
        # Установка разметки поля
        self.setColumnCount(len(content))
        self.setRowCount(len(content[list(content.keys())[0]]))
        # Подпись колонок столбцов
        self.setHorizontalHeaderLabels(content.keys())
        #  Наполнение таблицы данными
        for c_i, col in enumerate(content.keys()):
            for r_i, val in enumerate(content[col]):
                self.setItem(r_i, c_i, QTableWidgetItem(str(val)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = EditableTable()
    win.show()
    sys.exit(app.exec_())