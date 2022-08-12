from os import listdir

import os
import sys

# Импорт файлов соседней директории
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from instruments.Serializer import JSONm

class Connection():
    def __str__(self) -> str:
        return self.name+' '+self.type
        
    
    def __init__(self, name, type, config) -> None:
        
        self.name, self.type, self.config = name, type, config

        pass



class ConnectionStore():
    def __str__(self) -> str:
        return "Description"
    
    def __init__(self) -> None:
        pass

    # Возвращает список сохраненных подключений в виде объектов Connection
    def get_connection_list(self) -> list:
        cl = []
        types = filter(lambda f: f.endswith(".json") , listdir('data/connections'))
        for typ in types:
            cl.extend([Connection(key, typ[:-5], val ) for key, val in JSONm.read(f'data/connections/{typ}').items() ] )
        return cl

    def get_connection_names(self, driver:str) -> list:
        try:
            return JSONm.read(f'data/connections/{driver}.json').keys()
        except FileNotFoundError:
            return []
            
    # Обновляет или добавляет соединение
    def add_or_update_connection(self, new_con:Connection):
        old_dict = JSONm.read(f'data/connections/{new_con.type}.json')
        old_dict[new_con.name] = new_con.config
        JSONm.write(f'data/connections/{new_con.type}.json', old_dict)





def main():


    cs = ConnectionStore()
    
    nc = Connection('ultra', 'sqlite', {
        "drivername": "sqlite",
        "database": "E:\\ImpFiles\\pyqt_apps\\new\\practica\\database-manager\\fefef.db"
    })

    print(cs.get_connection_names("wdwd"))

    pass


if __name__ == '__main__':
    main()