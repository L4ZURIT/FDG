from pprint import pprint
from PyQt5.uic import *
from PyQt5.QtWidgets import *
import sys

import os
import sys



# Импорт файлов соседней директории
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from component.DBEngineConnector import Connector
from component.MessageController import Messenger as msg
from instruments.PyQtSampler import EditableTable


class EditorGUI(QWidget):
    """
        Описание
        """
    
    # Буферы хранения запросов
    delete_rows = {}
    update_rows = {}
    insert_rows = {}

    def __init__(self, connector:Connector, parent=None):
        super().__init__(parent)
        loadUi('views/editorGUI.ui',self)
        # Объекты загруженного интрефейса
        self.lw_tables:QListWidget
        self.tw_p_table_data:QWidget
        self.tw_p_constraints:QWidget
        self.tw_p_combinations:QWidget
        self.vlo_for_table:QVBoxLayout
        self.tblw_content = EditableTable()
        self.pb_data_insert_row:QPushButton
        self.pb_data_delete_row:QPushButton
        self.pb_data_cancel:QPushButton
        self.pb_data_save:QPushButton

        # Остальные объекты        
        self.con:Connector = connector

        #Подключение сигналов
        self.lw_tables.itemDoubleClicked.connect(self.set_current_table)
        self.tblw_content.itemTextChanged.connect(self.update_row_cortage)
        self.pb_data_delete_row.clicked.connect(self.delete_row_cortage)
        self.pb_data_save.clicked.connect(self.commit_changes)
        self.pb_data_cancel.clicked.connect(self.decline_changes)
        #Настройка интерфейса
        self.lw_tables.addItems(self.con.table_names())
        self.vlo_for_table.addWidget(self.tblw_content)
        
        
    def set_current_table(self, item:QListWidgetItem):
        """
        Описание
        """
        # Устанавливаем текущую таблицу для работы с объектом Connector
        self.con.set_current_table(item.text())
        # Передаем данные таблицы в виджет на время отключая обработку изменений содержимого 
        self.tblw_content.itemTextChanged.disconnect(self.update_row_cortage)
        self.tblw_content.set_content(self.con.get_table())
        self.tblw_content.itemTextChanged.connect(self.update_row_cortage)
        # Передаем данные о свойствах в виджет
        ...
        # Передаем данные о комбинациях в виджет
        ...

    def update_row_cortage(self, item:QTableWidgetItem):
        """
        Описание 
        """
        if item.row() not in self.delete_rows.keys():
            # получаем новые данные кортежа
            vals = [i.text() for i in [self.tblw_content.item(item.row(), col) for col in range(self.tblw_content.columnCount())]]
            new_val = { column:value for column, value in zip(self.tblw_content.content.keys(), vals)}
            # получаем старые данные кортежа и маркируем изменения в таблице
            old_val = self.tblw_content.updated_row(item.row())
            # сохраняем обновление в список изменений
            self.update_rows[item.row()] = self.con.update_cortage(old_val, new_val)

    def delete_row_cortage(self):
        """
        Описание 
        """
        for row in self.tblw_content.selectedItems():
            val = self.tblw_content.deleted_row(row.row())
            self.delete_rows[row.row()] = self.con.delete_cortage(val)
            if row.row() in list(self.update_rows.values()):
                del self.update_rows[row.row()]
        




    # Подтверждение всех совершенных изменений 

    def commit_changes(self):
        """
        Описание 
        """

        print(self.update_rows, self.delete_rows)

        # Специальный буфер ответных сообщений от sqlalhemy, возвращаемых после запроса
        statuses = []
        statuses.append([self.con.request(self.update_rows[key]) for key in  self.update_rows.keys()])
        statuses.append([self.con.request(self.delete_rows[key]) for key in  self.delete_rows.keys()])

        # Если это непустые сообщения выводим их на экран в сообщении (обычно это сообщения об ошибках)
        for status in statuses:
            if type(status) != str and status != "no_data":
                for s in status:
                    if s != "no_data":
                        msg.err("Ошибка запроса:\n"+str(status))
        
        self.decline_changes()


    # Оклонение всех совершенных изменений 

    def decline_changes(self):
        """
        Описание 
        """
        # очищаем словари
        self.update_rows = {}
        self.delete_rows = {}

        # перезагружаем таблицу с новыми данными
        self.set_current_table(QListWidgetItem(self.con.currentTable.name))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = EditorGUI(Connector({
        "drivername": "postgresql",
        "host": "localhost",
        "port": "5432",
        "username": "postgres",
        "password": "5924",
        "database": "first_lab"
    }))
    win.show()
    sys.exit(app.exec_())