#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
import csv
import os
import sqlite3
from pandas import DataFrame


class DB:
    def __init__(self, db_path, dump_path_csv, dump_path_xlsx):
        super(DB, self).__init__()
        self.__db_path = db_path
        self.__dump_path = dump_path_csv
        self.__dump_path_xlsx = dump_path_xlsx
        self.__fields = ['ID', 'Никнейм', 'Имя', 'Фамилия', 'Номер телефона']
        self.cursor = None
        self.db = None
        self.init()

    def init(self):
        if not os.path.exists(self.__db_path):
            self.db = sqlite3.connect(self.__db_path, check_same_thread=False)
            self.cursor = self.db.cursor()
            self.cursor.execute('''CREATE TABLE users(
                            user_id text,
                            nick_name text,
                            name text,
                            last_name text,
                            phone text,
                            is_admin text,
                            UNIQUE (user_id, nick_name, name, last_name, phone)
                            )
                            ''')
            self.db.commit()
        else:
            self.db = sqlite3.connect(self.__db_path, check_same_thread=False)
            self.cursor = self.db.cursor()

    def db_write(self, user_id, nick_name, name, last_name, phone, is_admin):
        self.cursor.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)', (user_id, nick_name, name, last_name, phone, is_admin))
        self.db.commit()

    def db_read(self, user_id):
        self.cursor.execute(f'SELECT is_admin FROM users WHERE user_id = "{user_id}"')
        return self.cursor.fetchone()

    def db_export_csv(self):
        self.cursor.execute('SELECT user_id, nick_name, name, last_name, phone FROM users')
        data = self.cursor.fetchall()
        with open(self.__dump_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Никнейм', 'Имя', 'Фамилия', 'Номер телефона'])
            writer.writerows(data)

    def db_export_xlsx(self):
        d = {'ID': [], 'Никнейм': [], 'Имя': [], 'Фамилия': [], 'Номер телефона': []}
        self.cursor.execute('SELECT user_id, nick_name, name, last_name, phone FROM users')
        users = self.cursor.fetchall()
        for user in users:
            for info in range(len(list(user))):
                d[self.__fields[info]].append(user[info])
        df = DataFrame(d)
        df.to_excel(self.__dump_path_xlsx, sheet_name='пользователи', index=False)

    def quantity_records(self):
        self.cursor.execute('SELECT COUNT(*) FROM users')
        quantity = list(self.cursor.fetchone())
        return quantity[0]
