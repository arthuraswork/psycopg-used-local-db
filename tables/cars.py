# Таблица персоны и особые действия с ней

from dbtable import *

class CarsTableModel(DbTable):
    table_name = 'cars'

    def __init__(self):
        super().__init__()


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
    
    def inserting_data(self):
        return [
    ('Kia', 'А123АА777', '#FF0000', 'economy', 2020),
    ('Hyundai', 'В234ВВ777', '#00FF00', 'comfort', 2021),
    ('Skoda', 'Е345ЕЕ777', '#0000FF', 'business', 2022),
    ('Volkswagen', 'К456КК777', '#FFFF00', 'comfort', 2019),
    ('BMW', 'М567ММ777', '#FF00FF', 'business', 2023),
    ('Toyota', 'Н678НН123', '#00FFFF', 'economy', 2021),
    ('Mercedes', 'О789ОО123', '#C0C0C0', 'business', 2022),
    ('Lada', 'Р890РР123', '#800000', 'economy', 2020),
    ('Nissan', 'С901СС123', '#008000', 'comfort', 2021),
    ('Audi', 'Т012ТТ123', '#000080', 'business', 2023)
]