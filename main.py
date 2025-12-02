import sys
sys.path.append('tables')

from project_config import *
from dbconnection import *
from tables.drivers import *
from tables.cars import *

class Main:

    config = ProjectConfig()
    connection = DbConnection(config)
    CarsTable = CarsTableModel()
    DriversTable = DriversTableModel()
    instance = '0'
    confirmed_ops = ['<','>','>=','<=','<>','=']
    count = 12

    def __init__(self):
        DbTable.dbconn = self.connection
        self.tables = [self.CarsTable, self.DriversTable]
    
    def insert_some_data(self):
        dt_data = [[(c,v) for c,v in zip(list(self.DriversTable.columns().keys())[1:],row)] for row in self.DriversTable.inserting_data()]
        ct_data = [[(c,v) for c,v in zip(list(self.CarsTable.columns().keys())[1:],row)] for row in self.CarsTable.inserting_data()]
        for dt,ct in zip(dt_data,ct_data):
            self.DriversTable.insert_one(dt)
            self.CarsTable.insert_one(ct)
    def input_processing(self, userinput):
        if len(userinput) >= 2 and userinput not in ['1+','2+']:
            userinput = userinput[1:]
        cmds = {
            '0': self.show_main_menu,
            '1': self.show_drivers,
            '1+': self.add_driver,
            '2+': self.add_car,
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
            result = self.DriversTable.first()
        elif self.instance == '2':
            result = self.CarsTable.first()
        if result:
            self.print_result(result)
        else:
            print('Операция не дала результата')
            

    def select_last(self):
        result = None
        if self.instance == '1':
            result = self.DriversTable.last()
        elif self.instance == '2':
            result = self.CarsTable.last()
        if result:
            self.print_result(result)
        else:
            print('Операция не дала результата')

    def convert_number_to_id(self, print_res=False):
        num = str(int(input('Введите порядковый номер\n~$ ')) + 1)
        if not num.isdigit():
            print('Ошибка, для поиска по строковым значениям используйте 1?')
            return 
        rows = self.DriversTable.all(limit=num) if self.instance == '1' else self.CarsTable.all(limit=num)
        if (rows_count := len(rows)) == int(num):
            if print_res:
                return self.print_result(result=[rows[-1]])
            return rows[-1]

        print(f'Такой записи нет: записей всего {rows_count-1}')
        return []

    def create_tables(self):
        for table in self.tables:
            table.create(
                f"""
        CREATE TABLE IF NOT EXISTS {table.table_name}(
        
            {
                ', '.join([f"{column} {' '.join(constraints)}" for column, constraints in table.columns().items()])
                }
        
        )
                """
            )
    def db_init(self):
        self.DriversTable.create()
        self.CarsTable.create()
        return

    def db_drop(self):
        if self.instance == '1':
            self.DriversTable.drop()
            return
        self.CarsTable.drop()
        

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
        lst = self.DriversTable.all()
        return self.print_result(lst)

    def print_result(self, result:list):
        keys = None
        if self.instance == '1':
            keys = list(self.DriversTable.columns().keys())[1:]
        if self.instance == '2':
            keys = list(self.CarsTable.columns().keys())[1:]    
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
            result = self.DriversTable.select_where(x, operation, val)
        elif self.instance == '2':
            result = self.CarsTable.select_where(x, operation, val)
        
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
        lst = self.CarsTable.all()
        return self.print_result(lst)

    def add_driver(self):

        data = []

        for column, datatype in self.DriversTable.columns().items():
            maxlen = 64
            if '(' in datatype[0]:
                maxlen = int(''.join([i for i in datatype[0] if i.isdigit()]))

            if datatype[0] != 'serial':
                while True:
                    user_input = input(f"Введите данные в {column}: {datatype[0]}\n~$ ").strip()

                    if column == 'inn' and (len(user_input) != 12 or not user_input.isdigit()):
                        print('ИНН состоит только из цифр и длина == 12')
                        continue
                    
                    elif column == 'pasport_series' and (len(user_input) != 4 or not user_input.isdigit()):
                        print('Серия паспорта состоит только из цифр и длина == 4')
                        continue
                    
                    elif column == 'pasport_number' and (len(user_input) != 6 or not user_input.isdigit()):
                        print('Номер паспорта состоит только из цифр и длина == 6')
                        continue
                    
                    elif column == 'birth_date':
                        parts = user_input.split('-')
                        if len(parts) != 3:
                            print('Формат даты: ГГГГ-ММ-ДД')
                            continue
                        year, month, day = parts
                        if not (year.isdigit() and month.isdigit() and day.isdigit()):
                            print('Дата должна содержать только цифры')
                            continue
                        if not (1900 <= int(year)):
                            print('Год должен быть не меньше 1900')
                            continue

                    if len(user_input) > maxlen or len(user_input) < 1:
                        print(f'Длинна ввода должна быть меньше {maxlen} и больше ноля')
                    else:
                        data.append((column,user_input))          
                        break
        self.DriversTable.insert_one(data)
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
            result = self.DriversTable.delete_where(x, operation, val)
        elif self.instance == '2':
            result = self.CarsTable.delete_where(x, operation, val)
        
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
        current_table = self.DriversTable if self.instance == '1' else self.CarsTable
        datatype = current_table.columns().get(updating_column)
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
            result = self.DriversTable.update_table(x, operation, val, updating_column, new_value)
        elif self.instance == '2':
            result = self.CarsTable.update_table(x, operation, val, updating_column, new_value)
        
        if result:
            self.print_result(
                result=result
            )
        else:
            print('Операция не дала результата')


    
    def add_car(self):
        data = []

        for column, datatype in self.CarsTable.columns().items():
            maxlen = 64
            if '(' in datatype[0]:
                maxlen = int(''.join([i for i in datatype[0] if i.isdigit()]))

            if datatype[0] != 'serial':
                while True:
                    user_input = input(f"Введите данные в {column}: {datatype[0]}\n~$ ").strip()

                    if column == 'number' and (len(user_input) != 9 or not self.is_valid_car_number(user_input)):
                        print('Номер машины должен быть 9 символов (пример: А123АА777)')
                        continue
                    
                    elif column == 'color_hex' and (len(user_input) != 7 or not user_input.startswith('#')):
                        print('Цвет в формате HEX: #RRGGBB')
                        continue
                    
                    elif column == 'production_year' and (not user_input.isdigit() or not 1900 <= int(user_input) <= 2024):
                        print('Год производства должен быть числом 1900-2024')
                        continue
                    if len(user_input) > maxlen or len(user_input) < 1:
                        print(f'Длинна ввода должна быть меньше {maxlen} и больше ноля')
                    else:
                        data.append((column,user_input))          
                        break
        self.CarsTable.insert_one(data)
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
if __name__ == "__main__":
    #m.test()
    #m.insert_some_data()
    m.main_cycle()
