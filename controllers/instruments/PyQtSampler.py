from pprint import pprint
from turtle import update
from PyQt5.uic import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QColor
import sys



class EditableTable(QTableWidget):

    content = {}

    def __init__(self, parent = None) -> None:
        super().__init__(parent)

    # Заполняет таблицу полученными данными
    def set_content(self, content:dict):
        
        self.content = content
        """
        Описание
        """
        # Установка разметки поля
        self.setColumnCount(len(content))
        self.setRowCount(len(content[list(content.keys())[0]]))
        # Подпись колонок столбцов
        self.setHorizontalHeaderLabels(content.keys())
        #  Наполнение таблицы данными
        for c_i, col in enumerate(content.keys()):
            for r_i, val in enumerate(content[col]):
                self.setItem(r_i, c_i, QTableWidgetItem(str(val)))
        
    

    def updated_row(self, row_index:int) -> dict:
        """
        Описание 
        """
        for col in range(self.columnCount()):
            self.item(row_index, col).setBackground(QColor.fromRgb(255,165,0))
        return {column:value for column, value in zip(list(self.content.keys()), [self.content[k][row_index] for k in self.content.keys()])}


    def deleted_row(self, row_index) -> dict:
        """
        Описание 
        """
        for col in range(self.columnCount()):
            self.item(row_index, col).setBackground(QColor.fromRgb(255,0,0))
        return {column:value for column, value in zip(list(self.content.keys()), [self.content[k][row_index] for k in self.content.keys()])}


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = EditableTable()
    win.show()
    sys.exit(app.exec_())