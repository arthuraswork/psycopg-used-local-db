# Таблица персоны и особые действия с ней

from dbtable import *

class CarsTable(DbTable):
    def table_name(self):
        return  "cars"
    def columns(self):
        return {
            "id": ["serial", "PRIMARY KEY"],
            "brand": ["varchar(64)", "NOT NULL"],
            "number": ["varchar(9)", "NOT NULL", "UNIQUE"],
            "color_hex": ["varchar(7)", "NOT NULL"],
            "class": ["varchar(16)", "NOT NULL"],
            "production_year": ["integer", "NOT NULL"]
        }

    def find_by_position(self, num):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        sql += " LIMIT 1 OFFSET %(offset)s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"offset": num - 1})
        return cur.fetchone()       
    
