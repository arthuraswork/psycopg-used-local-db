

from dbtable import *

class DriversTableModel(DbTable):
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
    ('Иван', 'Петров', 'Сергеевич', '1985-03-15', '770112345678', '4510', '123456'),
    ('Алексей', 'Сидоров', 'Владимирович', '1990-07-22', '770198765432', '4511', '654321'),
    ('Мария', 'Иванова', 'Алексеевна', '1988-11-30', '770123456789', '4512', '234567'),
    ('Дмитрий', 'Кузнецов', 'Петрович', '1983-05-14', '770134567890', '4513', '345678'),
    ('Сергей', 'Смирнов', 'Дмитриевич', '1992-09-08', '770145678901', '4514', '456789'),
    ('Ольга', 'Васильева', 'Сергеевна', '1987-12-25', '770156789012', '4515', '567890'),
    ('Андрей', 'Попов', 'Игоревич', '1986-01-19', '770167890123', '4516', '678901'),
    ('Екатерина', 'Новикова', 'Андреевна', '1991-04-03', '770178901234', '4517', '789012'),
    ('Павел', 'Федоров', 'Олегович', '1984-08-11', '770189012345', '4518', '890123'),
    ('Анна', 'Морозова', 'Викторовна', '1989-06-28', '770190123456', '4519', '901234')
]