import psycopg2

class Authentication_Table:

    def __init__(self, 
            host = 'localhost', 
            database = 'authentication_table',
            user = 'postgres',
            password = '12345678'
            ):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.conn = None
        self.cur = None

        self.connect()
        self.create_tables()

    # Подключение к БД
    def connect(self):
        self.conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )
        self.cur = self.conn.cursor()
    
    # Создание таблицы
    def create_tables(self):
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS log_pas (
            id SERIAL PRIMARY KEY,
            login VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        )
        ''')
        self.conn.commit()

    # ОПАСНО Полная чистка от записей!!!
    def WARNING_drop_data(self):
        self.cur.execute('''
        TRUNCATE TABLE log_pas
        ''')
        self.conn.commit()

    # Проверка условий регистрации или входа
    def sign_in_or_check(self, login, password, command):
        if command == 'REGISTRATION':
            if self.check_user(login):
                return("Такое имя пользователя уже существует")
            else:
                self.add_user(login, password)
                return("Пользователь успешно зарегистрирован")
        elif command == 'SIGN_IN':
            if self.check_log_pas(login, password):
                return('Вход выполнен успешно')
            else:
                return('Неверный логин или пароль')
    
    # Проверка на наличие пользователя с заданым логином и паролем
    def check_log_pas(self, log, pas):
        self.cur.execute('''
        SELECT login FROM log_pas
        WHERE login = %s
        AND password = %s
        ''', (log, pas, ))
        rows = self.cur.fetchall()
        if len(rows) > 0:
            return True
        else:
            return False

    # Проверка на наличие пользователя с заданным логином в БД
    def check_user(self, log):
        self.cur.execute('''
        SELECT login FROM log_pas
        WHERE login = %s
        ''', (log, ))
        rows = self.cur.fetchall()
        if len(rows) > 0:
            return True
        else:
            return False

    # Добавление пользователя с заданными логином и паролем
    def add_user(self, log, pas):
        self.cur.execute('''
        INSERT INTO log_pas(login, password)
        VALUES(%s, %s)
        ''', (log, pas, ))
        self.conn.commit()

    def close_connection(self):
        self.cur.close()
        self.conn.close()

    # удаление пользователя с заданным логином
    def delete_user(self, log):
        self.cur.execute('''
        DELETE FROM log_pas
        WHERE login = %s
        ''', (log, ))
        self.conn.commit()
        print('Пользователь успешно удален')
        
# ИСПОЛЬЗОВАНИЕ
# Создание БД
# my_database = Authentication_Table()

# ПРИМЕР
# Вывод результата выполнения команды (На входе логин, пароль и REGISTRATION или SIGN_IN)
# print(my_database.sign_in_or_check('Иван2233232322', 'qwer', 'REGISTRATION'))
