import sys
sys.path.append('tables')

from project_config import *
from dbconnection import *
from tables.drivers import *
from tables.cars import *

class Main:

    config = ProjectConfig()
    connection = DbConnection(config)
    ct = CarsTable('cars')
    dt = DriversTable('drivers')

    def __init__(self):
        DbTable.dbconn = self.connection
        return

    def db_init(self):

        self.ct.create()
        self.dt.create()
        return

    def db_drop(self):
        pht = DriversTable()
        pt = CarsTable()
        pht.drop()
        pt.drop()
        return

    def show_main_menu(self):
        menu = """
Добро пожаловать! 
Основное меню (выберите цифру в соответствии с необходимым действием): 
    1 - просмотр людей;
    2 - сброс и инициализация таблиц;
    3 - показ автомобилей;
    0 - выход.
"""
        print(menu)
        return

    def read_next_step(self):
        return input("=> ").strip()

    def after_main_menu(self, next_step):
        if next_step == "2":
            self.db_drop()
            self.db_init()
            self.db_insert_somethings()
            print("Таблицы созданы заново!")
            return "0"
        elif next_step != "1" and next_step != "9":
            print("Выбрано неверное число! Повторите ввод!")
            return "0"
        else:
            return next_step
            
    def show_people(self):
        self.person_id = -1
        menu = """Просмотр списка людей!
        
        """
        count = 8
        print(menu)
        lst = self.dt.all()
        print(
            "\t".join([f"\033[34m{i}{' '* (count -len(str(i)))}\033[0m" for i in self.dt.columns().keys()])
              )
        for i in lst:
            print("\t".join([f"{v}{' '* (count -len(str(v)))}" for v in i]))
        menu = """Дальнейшие операции: 
    0 - возврат в главное меню;
    3 - добавление нового водителя;
    4 - удаление водителя;
    5 - просмотр телефонов человека;
    9 - выход."""
        print(menu)
        return

    def after_show_people(self, next_step):
        while True:
            if next_step == "4":
                print("Пока не реализовано!")
                return "1"
            elif next_step == "6" or next_step == "7":
                print("Пока не реализовано!")
                next_step = "5"
            elif next_step == "5":
                next_step = self.show_phones_by_people()
            elif next_step != "0" and next_step != "9" and next_step != "3":
                print("Выбрано неверное число! Повторите ввод!")
                return "1"
            else:
                return next_step

    def show_add_driver(self):
        # Не реализована проверка на максимальную длину строк. Нужно доделать самостоятельно!
        data = []

        for column, datatype in self.dt.columns().items():
            maxlen = 64
            if '(' in datatype[0]:
                maxlen = int(''.join([i for i in datatype[0] if i.isdigit()]))

            if datatype[0] != 'serial':
                while True:
                    user_input = input(f"Введите данные в {column}: {datatype[0]}\n~$").strip()
                    if len(user_input) > maxlen or len(user_input) < 1:
                        print(f'Длинна ввода должна быть меньше {maxlen} и больше ноля')
                    else:
                        data.append((column,user_input))          
                        break
        self.dt.insert_one(data)
        return

    def show_phones_by_people(self):
        if self.person_id == -1:
            while True:
                num = input("Укажите номер строки, в которой записана интересующая Вас персона (0 - отмена):")
                while len(num.strip()) == 0:
                    num = input("Пустая строка. Повторите ввод! Укажите номер строки, в которой записана интересующая Вас персона (0 - отмена):")
                if num == "0":
                    return "1"
                person = CarsTable().find_by_position(int(num))
                if not person:
                    print("Введено число, неудовлетворяющее количеству людей!")
                else:
                    self.person_id = int(person[1])
                    self.person_obj = person
                    break
        print("Выбран человек: " + self.person_obj[2] + " " + self.person_obj[0] + " " + self.person_obj[3])
        print("Телефоны:")
        lst = DriversTable().all_by_person_id(self.person_id)
        for i in lst:
            print(i[1])
        menu = """Дальнейшие операции:
    0 - возврат в главное меню;
    1 - возврат в просмотр людей;
    6 - добавление нового телефона;
    7 - удаление телефона;
    9 - выход."""
        print(menu)
        return self.read_next_step()


    def main_cycle(self):
        current_menu = "0"
        next_step = None
        while(current_menu != "9"):
            if current_menu == "0":
                self.show_main_menu()
                next_step = self.read_next_step()
                current_menu = self.after_main_menu(next_step)
            elif current_menu == "1":
                self.show_people()
                next_step = self.read_next_step()
                current_menu = self.after_show_people(next_step)
            elif current_menu == "2":
                self.show_main_menu()
            elif current_menu == "3":
                self.show_add_driver()
                current_menu = "1"
        print("До свидания!")    
        return

    def test(self):
        DbTable.dbconn.test()

m = Main()
# Откоментируйте эту строку и закоментируйте следующую для теста
# соединения с БД
#print(m.test())

m.main_cycle()
    
