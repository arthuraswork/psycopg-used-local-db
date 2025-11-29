

from dbtable import *

class DriversTable(DbTable):
    table_name = 'drivers'

    def __init__(self):
        super().__init__()

    def columns(self):
        return {
            "id": ["serial", "PRIMARY KEY"],
            "name": ["varchar(32)", "NOT NULL"],
            "surname": ["varchar(32)", "NOT NULL"],
            "patronymic": ["varchar(32)"],
            "birth_date": ["date", "NOT NULL"],
            "inn": ["varchar(12)", "NOT NULL", "UNIQUE"],
            "pasport_series": ["varchar(4)", "NOT NULL"],
            "pasport_number": ["varchar(6)", "NOT NULL"]
        }
        
    def table_constraints(self):
        return ["PRIMARY KEY(id)"]



    def all_by_person_id(self, pid):
        sql = "SELECT * FROM " + self.table_name()
        sql += " WHERE id = %s"
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, str(pid))
        return cur.fetchall()           


    def inserting_data(self):
        return [
        ('Авраам', 'Коэн', 'Йосефович', '1980-03-15', '123456789012', '1234', '123456'),
        ('Сара', 'Аран', 'Абрамовна', '1985-07-22', '234567890123', '2345', '234567'),
        ('Ицхак', 'Гольдберг', 'Шмуэлевич', '1978-11-30', '345678901234', '3456', '345678'),
        ('Рахель', 'Кац', 'Соломоновна', '1990-01-10', '456789012345', '4567', '456789'),
        ('Иешуа', 'Ганоцриев', 'Иеговович', '1982-05-18', '567890123456', '5678', '567890'),
        ('Мария', 'Леви', 'Иоакимовна', '1975-09-05', '678901234567', '6789', '678901'),
        ('Давид', 'Ягода', 'Иесеевич', '1988-12-12', '789012345678', '7890', '789012'),
        ('Шломо', 'Ягода', 'Давидович', '1992-04-08', '890123456789', '8901', '890123'),
        ('Раби', 'Зильберман', 'Петрович', '1983-06-25', '901234567890', '9012', '901234'),
        ('Хая', 'Эпштейн', 'Яковлевна', '1987-08-14', '012345678901', '0123', '012345')
        ]