import sys
sys.path.append('tables')

from project_config import *
from dbconnection import *
from tables.drivers import *
from tables.cars import *

class Main:

    config = ProjectConfig()
    connection = DbConnection(config)
    ct = CarsTable()
    dt = DriversTable()
    instance = '0'
    confirmed_ops = ['<','>','>=','<=','<>','=']
    count = 12

    
    def __init__(self):
        DbTable.dbconn = self.connection
        self.tables = [self.ct, self.dt]
        return

    def input_processing(self, userinput):
        if len(userinput) >= 2:
            userinput = userinput[1]
        cmds = {
            '0': self.show_main_menu,
            '1': self.show_drivers,
            '+': self.add_driver,
            '2': self.show_cars,
            '?': self.select_by_x,
            '!': self.update_by_x,
            'f': self.select_first,
            'l': self.select_last,
            '-': self.delete_by_x,
            '3': self.create_tables,
            '*0': self.db_drop,
            'n': self.convert_number_to_id
        }

        func = cmds.get(userinput)
        if func:
            if userinput == 'n':
                return func(True)
            return func()
    
    def select_first(self):
        result = None
        if self.instance == '1':
            result = self.dt.first()
        elif self.instance == '2':
            result = self.ct.first()
        if result:
            self.print_result(result)
        else:
            print('Операция не дала результата')
            

    def select_last(self):
        result = None
        if self.instance == '1':
            result = self.dt.last()
        elif self.instance == '2':
            result = self.ct.last()
        if result:
            self.print_result(result)
        else:
            print('Операция не дала результата')

    def convert_number_to_id(self, print_res=False):
        num = str(int(input('Введите порядковый номер\n~$ ')) + 1)
        if not num.isdigit():
            print('Ошибка, для поиска по строковым значениям используйте 1?')
            return 
        rows = self.dt.all(limit=num) if self.instance == '1' else self.ct.all(limit=num)
        if (rows_count := len(rows)) == int(num):
            if print_res:
                return self.print_result(result=[rows[-1]])
            return rows[-1]

        print(f'Такой записи нет: записей всего {rows_count-1}')
        return []

    def create_tables(self):
        request = []
        for table in self.tables:
            request.append(
                f"""
        CREATE TABLE IF NOT EXISTS {table.name}(
        
            {
                ', '.join([f"{column} {' '.join(constraints)}" for column, constraints in table.columns().items()])
                }
        
        )
                """
            )

    def db_init(self):
        self.dt.create()
        self.dt.create()
        return

    def db_drop(self):
        if self.instance == '1':
            self.dt.drop()
            return
        self.dt.drop()
        

    def show_main_menu(self):
        menu = """
Добро пожаловать! 
Основное меню (выберите цифру в соответствии с необходимым действием): 
    1 - просмотр людей;
    2 - просмотр автомобилей;
    3 - создание таблиц;
    9 - выход.
"""     
        print(menu)
        return

    def read_next_step(self):
        return input("=> ").strip()
            
    def show_drivers(self):
        print("Просмотр списка водителей:")
        lst = self.dt.all()
        return self.print_result(lst)

    def print_result(self, result:list):
        keys = None
        if self.instance == '1':
            keys = list(self.dt.columns().keys())[1:]
        if self.instance == '2':
            keys = list(self.ct.columns().keys())[1:]    
        if not keys:
            return
        result = [i[1:] for i in result]
        print("\033[34mНомер   ",
            "\t".join([f"{i}{' '* (self.count -len(str(i)))}" for i in keys],
                      ), 
                '\033[0m'
              )
        for i, row in enumerate(result):
            print(f'{i}\t', "\t".join([f"{v}{' '* (self.count -len(str(v)))}" for v in row]))

        print('\n')

            
    def select_by_x(self):
        result = None
        val = None

        print('Если вы хотите использовать номер для поиска, если номер, то введите n')
        num_or_else = input('~$ ')
        if num_or_else == 'n':
            result = self.convert_number_to_id()
            if not num_or_else:
                return 
            x = 'id'
            val = result[0]
        else:
            x = input('Введите колонку\n~$ ')
        operation = input('Введите операцию\n~$ ')
        if operation not in self.confirmed_ops:
            print('Используйте разрешенные операции:',', '.join(self.confirmed_ops))
            return     
        if not val:
            val = input('Введите значение\n~$ ') 
        if self.instance == '1':
            result = self.dt.select_where(x, operation, val)
        elif self.instance == '2':
            result = self.dt.select_where(x, operation, val)
        
        if result:
            self.print_result(
                result=result
            )
        else:
            print('Операция не дала результата')

    def table_menu(self,num):
        menu = f"""Дальнейшие операции: 
    0    возврат в главное меню;
    {num}+   добавление нового объекта;
    {num}-   удаление объекта;
    {num}f   первый объект;
    {num}l   последний объект;
    {num}*0  удаление таблицы;
    {num}?   поиск по столбцу и значению;
    {num}n   поиск по порядковому номеру;
    9    выход
    """
        print(menu)
    
    def show_cars(self):
        print("Просмотр списка машин:")
        lst = self.ct.all()
        return self.print_result(lst)

    def add_driver(self):

        data = []

        for column, datatype in self.dt.columns().items():
            maxlen = 64
            if '(' in datatype[0]:
                maxlen = int(''.join([i for i in datatype[0] if i.isdigit()]))

            if datatype[0] != 'serial':
                while True:
                    user_input = input(f"Введите данные в {column}: {datatype[0]}\n~$ ").strip()
                    if len(user_input) > maxlen or len(user_input) < 1:
                        print(f'Длинна ввода должна быть меньше {maxlen} и больше ноля')
                    else:
                        data.append((column,user_input))          
                        break
        self.dt.insert_one(data)
        return
    
    def delete_by_x(self):
        result = None
        val = None

        print('Если вы хотите использовать номер для поиска, если номер, то введите n')
        num_or_else = input('~$ ')
        if num_or_else == 'n':
            result = self.convert_number_to_id()
            if not num_or_else:
                return 
            x = 'id'
            val = result[0]
        else:
            x = input('Введите колонку\n~$ ')
        operation = input('Введите операцию\n~$ ')
        if operation not in self.confirmed_ops:
            print('Используйте разрешенные операции:',', '.join(self.confirmed_ops))
            return     
        if not val:
            val = input('Введите значение\n~$ ') 
        if self.instance == '1':
            result = self.dt.delete_where(x, operation, val)
        elif self.instance == '2':
            result = self.dt.delete_where(x, operation, val)
        
        if result:
            self.print_result(
                result=result
            )
        else:
            print('Операция не дала результата')


    def update_by_x(self):
        result = None
        val = None
        maxlen = 64
        print('Если вы хотите использовать номер для поиска, если номер, то введите n')
        num_or_else = input('~$ ')
        if num_or_else == 'n':
            result = self.convert_number_to_id()
            if not num_or_else:
                return 
            x = 'id'
            val = result[0]
        else:
            x = input('Введите колонку\n~$ ')
        operation = input('Введите операцию\n~$ ')
        if operation not in self.confirmed_ops:
            print('Используйте разрешенные операции:',', '.join(self.confirmed_ops))
            return     
        if not val:
            val = input('Введите значение\n~$ ') 

        updating_column = input('Введите обновляемую колонку\n~$ ')
        str_to_i = False
        datatype = self.dt.columns().get(updating_column)
        if datatype:
            if '(' in datatype[0]:
                maxlen = int(''.join([i for i in datatype[0] if i.isdigit()]))
                if 'integer' in datatype[0] or 'serial' in datatype[0]:
                    str_to_i = True
                    
        new_value = input('Введите новое значени\n~$ ')
        if str_to_i:
            new_value = int(new_value)

        if len(new_value) > maxlen or len(new_value) < 1:
            print(f'Длинна ввода должна быть меньше {maxlen} и больше ноля')
            return
        if self.instance == '1':
            result = self.dt.update_table(x, operation, val, updating_column, new_value)
        elif self.instance == '2':
            result = self.dt.update_table(x, operation, val, updating_column, new_value)
        
        if result:
            self.print_result(
                result=result
            )
        else:
            print('Операция не дала результата')


    
    def add_car(self):

        data = []

        for column, datatype in self.dt.columns().items():
            maxlen = 64
            if '(' in datatype[0]:
                maxlen = int(''.join([i for i in datatype[0] if i.isdigit()]))

            if datatype[0] != 'serial':
                while True:
                    user_input = input(f"Введите данные в {column}: {datatype[0]}\n~$ ").strip()
                    if len(user_input) > maxlen or len(user_input) < 1:
                        print(f'Длинна ввода должна быть меньше {maxlen} и больше ноля')
                    else:
                        data.append((column,user_input))          
                        break
        self.dt.insert_one(data)
        return

    def main_cycle(self):
        while(self.instance != "9"):
            try:
                self.show_main_menu() if self.instance not in ['1','2'] else self.table_menu(self.instance)
                userinput = input('>>> ')        
                self.instance = userinput[0]
                self.input_processing(userinput=userinput)
            except psycopg2.Error as bde:
                print('Произошла ошибка базы данных:', bde)
            except Exception as e:
                print('Произошла ошибка клиента:', e)
        print("До свидания!")    
        return

    def test(self):
        DbTable.dbconn.test()

m = Main()
m.main_cycle()
    
