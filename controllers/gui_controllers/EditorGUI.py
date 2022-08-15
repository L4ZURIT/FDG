from PyQt5.uic import *
from PyQt5.QtWidgets import *
import sys

import os
import sys



# Импорт файлов соседней директории
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from component.DBEngineConnector import Connector
from instruments.PyQtSampler import EditableTable


class EditorGUI(QWidget):
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
        # Остальные объекты        
        self.con:Connector = connector

        #Подключение сигналов
        self.lw_tables.itemDoubleClicked.connect(self.set_current_table)
        #Настройка интерфейса
        self.lw_tables.addItems(self.con.table_names())
        self.vlo_for_table.addWidget(self.tblw_content)
        
        
    def set_current_table(self, item:QListWidgetItem):
        # Устанавливаем текущую таблицу для работы с объектом Connector
        self.con.set_current_table(item.text())
        # Передаем данные таблицы в виджет
        self.tblw_content.set_content(self.con.get_table())
        # Передаем данные о совйствах в виджет
        ...
        # Передаем данные о комбинациях в виджет
        ...

    # Ты остановился тут


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