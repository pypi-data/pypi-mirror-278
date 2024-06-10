from dataclasses import dataclass
import sqlalchemy as sa
import urllib

@dataclass
class DBHelper:
    server: str
    trusted: bool = True
    
    def __post_init__(self):
        pass
    
    def connect_engine(self, db: str, echo: bool = True) -> None:
        self.engine = self.__db_connect(db, echo)
        self.insp = sa.inspect(self.engine)

    def close(self) -> None:
        self.engine.dispose()
    
    def __db_connect(self, db: str, echo: bool) -> sa.Engine:
        """Laver nogle ret hårde antagelser om db'en, som dog burde holde fremadrettet"""
        con_string = (
            f"DRIVER={{SQL Server}};"
            f"SERVER={self.server};"
            f"DATABASE={db};"
            f"trusted_Connection={self.trusted}"
        )
        quoted_con_string = urllib.parse.quote_plus(con_string)
        db_engine = sa.create_engine(
            f"mssql+pyodbc:///?odbc_connect={quoted_con_string}", use_setinputsizes=False, echo=echo
        )
        return db_engine
       
    
if __name__ == '__main__':
    source = DBHelper(server=r"C2100306\MSSQLSERVER01")
    try:
        source.connect_engine(r"1_PROD_COPY")
        print("Succes!")
    except sa.exc.ProgrammingError as err:
        print(err)
    source.close()
