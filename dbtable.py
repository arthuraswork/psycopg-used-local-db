# Базовые действия с таблицами

from dbconnection import *

class DbTable:
    dbconn = None
    table_name = 'table_name'
    primary_key = 'id'


    def column_names_without_id(self):
        res = sorted(self.columns().keys(), key = lambda x: x)
        if 'id' in res:
            res.remove('id')
        return res

    def columns(self):
        pass

    def table_constraints(self):
        return self.columns().values()

    def create(self, request):
        cur = self.dbconn.conn.cursor()
        cur.execute(request)
        self.dbconn.conn.commit()
        return

    def drop(self):
        sql = "DROP TABLE IF EXISTS " + self.table_name
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        return

    def update_table(self, x, op, val, upd_column, new_val):
        if x not in self.columns().keys() or upd_column not in self.columns().keys():
            print('Такой колонки нет')
            return  
        sql = f"UPDATE {self.table_name} SET {upd_column} = %s WHERE ({x} {op} %s) RETURNING *"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (new_val, val))
        self.dbconn.conn.commit()
        return cur.fetchall()

    def delete_where(self, x, op, val):
        if x not in self.columns().keys():
            print('Такой колонки нет')
            return  
        sql = f"DELETE FROM {self.table_name} WHERE ({x} {op} %s) RETURNING *"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (val,))
        self.dbconn.conn.commit()
        return cur.fetchall()

    def select_where(self, x, op, val):
        if x not in self.columns().keys():
            print('Такой колонки нет')
            return  
        sql = f"SELECT * FROM {self.table_name} WHERE ({x} {op} %s)"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (val,))
        return cur.fetchall()

    def insert_one(self, vals):
        values = ", ".join([c for c,_ in vals])
        data_placeholders = ", ".join(['%s' for _,v in vals])
        params = tuple([v for _,v in vals])
        sql = f"INSERT INTO {self.table_name} ({values}) VALUES ({data_placeholders})"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, params)
        self.dbconn.conn.commit()
        return

    def first(self):
        sql = "SELECT * FROM " + self.table_name
        sql += f" ORDER BY {self.primary_key} LIMIT 1"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return [cur.fetchone()]        


    def last(self):
        sql = "SELECT * FROM " + self.table_name
        sql += f" ORDER BY {self.primary_key} DESC LIMIT 1"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return [cur.fetchone()]    

    def all(self, limit = ''):
        if limit:
            limit = 'LIMIT ' + limit
        sql = "SELECT * FROM " + self.table_name
        sql += f" ORDER BY {self.primary_key} " + limit 
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()
        
