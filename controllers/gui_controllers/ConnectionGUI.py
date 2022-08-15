from PyQt5.uic import *
from PyQt5.QtWidgets import *

import os
import sys

# Импорт файлов соседней директории
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from instruments.Serializer import configm as cfg
from stores.ConnectionStore import Connection, ConnectionStore
from component.DBEngineConnector import Connector
from component.MessageController import Messenger as msg


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
        # для postgres
        self.le_postgres_host.textChanged.connect(self.postgres_check)
        self.le_postgres_port.textChanged.connect(self.postgres_check)
        self.le_postgres_un.textChanged.connect(self.postgres_check)
        self.le_postgres_pwd.textChanged.connect(self.postgres_check)
        self.le_postgres_database.textChanged.connect(self.postgres_check)
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
        # использовать Messenger
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

    def postgres_check(self):
        if any(
            (self.le_postgres_host.text().strip() == "",
            self.le_postgres_port.text().strip() == "",
            self.le_postgres_un.text().strip() == "",
            self.le_postgres_pwd.text().strip() == "",
            self.le_postgres_database.text().strip() == "")
        ):
            self.pb_ok.setEnabled(False)
        else:
            self.pb_ok.setEnabled(True)

    # Конфигурации
    def get_config(self, driver:str) -> dict:
        if driver == "sqlite":
            return self.get_config_sqlite()
        elif driver == "postgres":
            return self.get_config_postgres()
        # elif driver == "YourDriverName":
            # return get_config_your_config()

    def get_config_sqlite(self) -> dict:
        return {
            "drivername":"sqlite", 
            "database":self.le_sqlite_path.text().strip()
        } 

    def get_config_postgres(self) -> dict:
        return {
            "drivername": "postgresql",
            "host": self.le_postgres_host.text(),
            "port": self.le_postgres_port.text(),
            "username": self.le_postgres_un.text(),
            "password": self.le_postgres_pwd.text(),
            "database": self.le_postgres_database.text()
    }

    # def get_config_your_config():
        #...

   
    def connect(self):
        con_name = self.le_connection_name.text().strip()
        con_type = self.cb_driver_list.currentText()
        if con_name in self.CS.get_connection_names(con_type):
            if not msg.ask_y_n("Такое подключение уже существует вы хотите его перезаписать?"):
                return
        elif con_name == "":
            msg.err("Сначала укажите имя")
            return
        try:
            self.C = Connection(con_name, con_type, self.get_config(con_type))
            self.Cr = Connector(self.C.config)
        except Exception as ex:
            msg.err(str(ex))
            return
        self.CS.add_or_update_connection(self.C)     
        msg.say("Подключение сохранено")
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ConnectionGUI()
    win.show()
    sys.exit(app.exec_())