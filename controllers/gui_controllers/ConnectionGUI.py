from PyQt5.uic import *
from PyQt5.QtWidgets import *

import os
import sys

# Импорт файлов соседней директории
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from instruments.Serializer import configm as cfg
from stores.ConnectionStore import Connection, ConnectionStore
from component.DBEngineConnector import Connector


# Новые виджеты в стек добавлять в соотвествии с порядком добавления в конфигурации

class ConnectionGUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Опасный момент
        loadUi('views/connectionGUI.ui',self)
        # Объекты загруженного интерфейса
        self.cb_driver_list:QComboBox
        self.stackedWidget:QStackedWidget
        self.sw_p_sqlite:QWidget
        self.sw_p_postgres:QWidget
        # self.sw_p_new_dbdriver:QWidget
        self.pb_cancel:QPushButton
        self.pb_ok:QPushButton
        self.le_connection_name:QLineEdit
        #Переменные sqlite виджета соединения
        self.le_sqlite_path:QLineEdit
        self.pb_sqlite_find:QPushButton
        self.lbl_sqlite_status:QLabel
        #Переменные sqlite виджета соединения
        self.le_postgres_host:QLineEdit
        self.le_postgres_port:QLineEdit
        self.le_postgres_un:QLineEdit
        self.le_postgres_pwd:QLineEdit
        self.le_postgres_database:QLineEdit
        #Переменные ...
            #Добавить переменные нового виджета подключения
        
        # Остальные объекты
        self.CS = ConnectionStore()
        self.C:Connection = None
        self.Cr:Connector = None

        # Подключение сигналов
        self.cb_driver_list.currentIndexChanged.connect(self.driver_selected)
        self.pb_cancel.clicked.connect(self.clear_fields)
        self.pb_ok.clicked.connect(self.connect)
        # для sqlite
        self.pb_sqlite_find.clicked.connect(self.sqlite_find_path)
        self.le_sqlite_path.textChanged.connect(self.sqlite_check_path)
        # Переопределение событий
        
        

        # Настройка интерфейса
        self.cb_driver_list.addItems(cfg.availibale_db_drivers())
        self.pb_ok.setEnabled(False)
        self.cb_driver_list.setCurrentIndex(0)
        # Настройка виджета для sqlite
        self.lbl_sqlite_status.setText("")
    
    # Устанавливает виджет обработки подключения в зависимости от выбранного дравера
    def driver_selected(self):
        self.clear_fields()
        self.stackedWidget.setCurrentIndex(self.cb_driver_list.currentIndex())


    #Очищает вводимые пользователем данные
    def clear_fields(self):
        for wdg in self.stackedWidget.children():
            for le in wdg.children():
                if type(le) is QLineEdit: # or и добавить свои поля
                    le.clear()

    # Находит бд по указаному пути 
    def sqlite_find_path(self):
        file , check = QFileDialog.getOpenFileName(None, "Выбрать базу sqlite","", "Базы данных (*.db);;Базы данных (*.sqlite3)")
        if check:
            self.le_sqlite_path.setText(file)
        
    # Проверяет наличие файла
    def sqlite_check_path(self):
        if os.path.exists(self.le_sqlite_path.text()):
            self.lbl_sqlite_status.setText("Есть")
            self.pb_ok.setEnabled(True)
        else:
            self.lbl_sqlite_status.setText("Не найден")
            self.pb_ok.setEnabled(False)



    # Этап на котором ты остановился (почитай гит сначала)
    def connect(self):
        if self.le_connection_name.text().strip() in self.CS.get_connection_names(self.cb_driver_list.currentText()):
            # message Такая запись уже существует
            ...

        



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ConnectionGUI()
    win.show()
    sys.exit(app.exec_())