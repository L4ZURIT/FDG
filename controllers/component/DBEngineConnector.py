
from sqlalchemy import create_engine, Column, Table, MetaData, ForeignKey, select, inspect
from sqlalchemy.engine import Engine, reflection, Inspector
from sqlalchemy.orm import sessionmaker, Query, scoped_session
from sqlalchemy.engine.url import URL

class Connector():

    engine:Engine
    md:MetaData
    session:scoped_session
    insp:Inspector

    def __str__(self) -> str:
        return "Описание"

    def __init__(self, con_data:dict) -> None:
        self.engine = create_engine(URL.create(**con_data))
        self.md = MetaData(bind=self.engine)
        self.db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=self.engine))
        self.insp = inspect(self.engine)  
        self.table_names = self.insp.get_table_names

        pass







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
    print(c)
    print(c.table_names())


    pass


if __name__ == '__main__':
    main()