

from dbtable import *

class DriversTable(DbTable):
    def table_name(self):
        return "drivers"

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
        
    def primary_key(self):
        return ['id']    

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


