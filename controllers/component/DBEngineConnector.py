import pandas as pd
from sqlalchemy import create_engine, Column, Table, MetaData, ForeignKey, select, inspect, and_, text
from sqlalchemy.engine import Engine, reflection, Inspector
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker, Query, scoped_session
from sqlalchemy.exc import ResourceClosedError

class Connector():
    """
        Описание
    """

    engine:Engine
    md:MetaData
    session:scoped_session
    insp:Inspector
    currentTable:Table


    def __init__(self, con_data:dict) -> None:
        self.currentTable = None
        self.engine = create_engine(URL.create(**con_data), client_encoding = "UTF-8")
        self.md = MetaData(bind=self.engine)
        self.db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=self.engine))
        self.insp = inspect(self.engine)  
        self.table_names = self.insp.get_table_names
    
    def request(self, req):
        """
        Описание
        """
        conn = self.engine.connect()
        try:
            result = conn.execute(req)
        except Exception as ex:
            return ex
        try:
            return "\n".join([str(res) for res in result])
        except ResourceClosedError:
            return "no_data"

    def get_table(self) -> dict:
        """
        Возвращает таблицу в виде словаря с полями в виде ключей и списками значений

        table  = Connector.get_table()

        cortage = table['column']           # [value1, value2, value3]

        """
        req = self.currentTable.select()
        conn = self.engine.connect()
        res = conn.execute(req)
        tab = pd.DataFrame(res.fetchall())
        ans = tab.to_dict(orient='list')
        if ans == {}:
            ans = {str(col.name):[] for col in self.currentTable.columns}
        return ans

    def set_current_table(self, table_name:str):
        """
        Описание
        """
        self.currentTable = Table(table_name, self.md, autoload_with=self.engine)

    def update_cortage(self, old_values:dict, new_values:dict):
        """
        Описание
        """
        return self.currentTable.update().where(and_(
                    self.currentTable.c[pkc.name] == old_values[pkc.name] for pkc in self.currentTable.primary_key.columns
                    )).values(tuple(new_values.values()))
        
    def delete_cortage(self, vals:dict):
        """
        Описание
        """
        return self.currentTable.delete().where(
                and_(
                    self.currentTable.c[i.name] == vals[i.name]
                    for i in self.currentTable.primary_key.columns
                    ))

    def insert_cortage(self, vals:dict):
        """
        Описание
        """
        return self.currentTable.insert().values(tuple(vals[col.name] 
                    for col in self.currentTable.columns))




def main():

    # sqlite config
    db_config = {
        "drivername":"sqlite", 
        "database":"E:\\ImpFiles\\pyqt_apps\\new\\practica\\database-manager\\db.sqlite3"
    }

    db_config_pg = {
            "drivername": "postgresql",
            "host": "localhost",
            "port": "5432",
            "username": "postgres",
            "password": "5924",
            "database": "erp_system"
    }

    c = Connector(db_config_pg)
    
    print(c.md.tables)


    pass


if __name__ == '__main__':
    main()