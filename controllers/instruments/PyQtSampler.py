from PyQt5.uic import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QColor
import sys


"""
Хотел здесь написать декоратор для кратковремменного отключения слотов при изменении цвета ячеек, но что-то пошло не так. Точнее не могу сообразить как правильно его инициализировать, при создании класса EditableTable
"""

# def tumbler(func):
#     def wrapper(*args, **kwargs):

#         func(*args, **kwargs)

#     return wrapper



class EditableTable(QTableWidget):
    """
    Виджет для редактирования наполнения подключенной таблицы.
    """

    # Содержимое таблицы до внесения изменений
    content = {}
    
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        

    # Заполняет таблицу полученными данными
    def set_content(self, content:dict):
        """
        Заполняет таблицу данными из словаря, устанавливает в качестве имен столбцов, ключи словаря
        """
        self.content = content
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
        Маркирует указаную строку как "измененную" ОРАНЖЕВЫМ цветом и возвращает старые значения кортежа 
        """
        for col in range(self.columnCount()):
            self.item(row_index, col).setBackground(QColor.fromRgb(255,165,0))
        return {column:value for column, value in zip(list(self.content.keys()), [self.content[k][row_index] for k in self.content.keys()])}


    def deleted_row(self, row_index) -> dict:
        """
        Маркирует указаную строку как "удаленную" КРАСНЫМ цветом и возвращает старые значения кортежа 
        """
        for col in range(self.columnCount()):
            self.item(row_index, col).setBackground(QColor.fromRgb(255,0,0))
        return {column:value for column, value in zip(list(self.content.keys()), [self.content[k][row_index] for k in self.content.keys()])}

    def inserted_row(self) -> tuple:
        # реализовать заполнение значениями по умолчанию
        last_row = self.rowCount()
        values = {column:value for column, value in zip(list(self.content.keys()), list(self.content.keys()))}
        self.setRowCount(self.rowCount()+1)
        for col in range(self.columnCount()):
            self.setItem(last_row, col, QTableWidgetItem(values[list(values.keys())[col]]))
            self.item(last_row, col).setBackground(QColor.fromRgb(0,128,0))
        return last_row, values


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = EditableTable()
    win.show()
    sys.exit(app.exec_())