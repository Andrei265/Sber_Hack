import psycopg2
from datetime import datetime


class Main_Table:

    def __init__(self, 
            host = 'localhost', 
            database = 'main_table',
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
        # создание таблицы Test
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS Test (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                description VARCHAR(255),
                date_of_creation DATE
            );
        """)
        self.conn.commit()

        # создание таблицы Question
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS Question (
                id SERIAL PRIMARY KEY,
                number INTEGER,
                text VARCHAR(255),
                correct_answer VARCHAR(255),
                points INTEGER
            );
        """)
        self.conn.commit()
        
        # создание таблицы Applicant
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS Applicant (
            id SERIAL PRIMARY KEY,
            full_name VARCHAR(255),
            link_to_telegram VARCHAR(255),
            age VARCHAR(255),
            education VARCHAR(255),
            link_to_resume VARCHAR(255),
            skills VARCHAR(255),
            experience VARCHAR(255),
            schedule VARCHAR(255),
            employment VARCHAR(255),
            id_profession INTEGER
        )
        """)
        self.conn.commit()
        
        # создание таблицы Test_result
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS Test_result (
            id SERIAL PRIMARY KEY,
            id_test INTEGER,
            id_applicant INTEGER
        )
        """)
        self.conn.commit()
        
        # создание таблицы Answer
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS Answer (
            id SERIAL PRIMARY KEY,
            id_question INTEGER,
            response_text VARCHAR(255),
            is_the_answer_correct BOOLEAN
        )
        """)
        self.conn.commit()
        
        # создание таблицы Applicant_answers
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS Applicant_answers (
            id SERIAL PRIMARY KEY,
            id_question INTEGER,
            id_result INTEGER,
            id_answer INTEGER,
            score_for_the_answer INTEGER
        )
        """)
        self.conn.commit()
        
        # создание таблицы Author
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS Author (
            id SERIAL PRIMARY KEY,
            full_name VARCHAR(255),
            company VARCHAR(255),
            company_address VARCHAR(255),
            mail VARCHAR(255),
            phone VARCHAR(255)
        )
        """)
        self.conn.commit()
        
        # создание таблицы Authorship
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS Authorship (
            id_test INTEGER,
            id_author INTEGER
        )
        """)
        self.conn.commit()
        
        # создание таблицы Test_question
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS Test_question (
            id_question INTEGER,
            id_test INTEGER
        )
        """)
        self.conn.commit()
        
        # создание таблицы Profession
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS Profession (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            specialization VARCHAR(255),
            wage VARCHAR(255)
        )
        """)
        self.conn.commit()

        self.cur.execute('''
        ALTER TABLE Applicant 
        ADD CONSTRAINT Applicant_fk0 
        FOREIGN KEY (id_profession) 
        REFERENCES Profession(id)
        ''')
        
        self.cur.execute('''
        ALTER TABLE Test_result 
        ADD CONSTRAINT Test_result_fk0
        FOREIGN KEY (id_test) 
        REFERENCES Test(id)
        ''')
        self.cur.execute('''
        ALTER TABLE Test_result
        ADD CONSTRAINT Test_result_fk1
        FOREIGN KEY (id_applicant) 
        REFERENCES Applicant(id)
        ''')
        
        self.cur.execute('''
        ALTER TABLE Answer 
        ADD CONSTRAINT Answer_fk0 
        FOREIGN KEY (id_question) 
        REFERENCES Question(id)
        ''')

        self.cur.execute('''
        ALTER TABLE Applicant_answers 
        ADD CONSTRAINT Applicant_answers_fk0 
        FOREIGN KEY (id_question) 
        REFERENCES Question(id)
        ''')
        self.cur.execute('''
        ALTER TABLE Applicant_answers 
        ADD CONSTRAINT Applicant_answers_fk1 
        FOREIGN KEY (id_result) 
        REFERENCES Test_result(id)
        ''')
        self.cur.execute('''
        ALTER TABLE Applicant_answers 
        ADD CONSTRAINT Applicant_answers_fk2 
        FOREIGN KEY (id_answer) 
        REFERENCES Answer(id)
        ''')

        self.cur.execute('''
        ALTER TABLE Authorship 
        ADD CONSTRAINT Authorship_fk0 
        FOREIGN KEY (id_test) 
        REFERENCES Test(id)
        ''')
        self.cur.execute('''
        ALTER TABLE Authorship 
        ADD CONSTRAINT Authorship_fk1 
        FOREIGN KEY (id_author) 
        REFERENCES Author(id)
        ''')

        self.cur.execute('''
        ALTER TABLE Test_question 
        ADD CONSTRAINT Test_question_fk0 
        FOREIGN KEY (id_question) 
        REFERENCES Question(id)
        ''')
        self.cur.execute('''
        ALTER TABLE Test_question 
        ADD CONSTRAINT Test_question_fk1 
        FOREIGN KEY (id_test) 
        REFERENCES Test(id)
        ''')

    # ОПАСНО Полная чистка от записей!!!
    def WARNING_drop_data(self):
        self.cur.execute('''
        TRUNCATE TABLE log_pas
        ''')
        self.conn.commit()

    def close_connection(self):
        self.cur.close()
        self.conn.close()

    def return_list_soiskatelei(self):
        self.cur.execute('''
        SELECT FIO_soiskatelya, Ssilka_na_soiskatelya FROM Soiskateli
        ''')
        rows = self.cur.fetchall()
        return rows

    def get_id_profession(self, profession, specialization, wage):
        self.cur.execute('''
        SELECT id FROM Profession
        WHERE name = %s
        AND specialization = %s
        AND wage = %s
        ''', (profession, specialization, wage, ))
        rows = self.cur.fetchall()
        return str(rows[0])

    def get_id_test(self, name, description, date_of_creation):
        self.cur.execute('''
        SELECT id FROM Test
        WHERE name = %s
        AND description = %s
        AND date_of_creation = %s
        ''', (name, description, date_of_creation, ))
        rows = self.cur.fetchall()
        return str(rows[0])

    def get_id_author(self, mail):
        self.cur.execute('''
        SELECT id FROM Author
        WHERE mail = %s
        ''', (mail, ))
        rows = self.cur.fetchall()
        return str(rows[0])

    def get_id_applicant(self, link_to_telegram):
        self.cur.execute('''
        SELECT id FROM Applicant
        WHERE link_to_telegram = %s
        ''', (link_to_telegram, ))
        rows = self.cur.fetchall()
        return str(rows[0])

    def get_id_question(self, number, text, correct_answer, points):
        self.cur.execute('''
        SELECT id FROM Question
        WHERE number = %s
        AND text = %s
        AND correct_answer = %s
        AND points = %s
        ''', (number, text, correct_answer, points, ))
        rows = self.cur.fetchall()
        return str(rows[0])

    def get_id_answer(self, id_question, responce_text, is_the_answer_correct):
        self.cur.execute('''
        SELECT id FROM Answer
        WHERE id_question = %s
        AND responce_text = %s
        AND is_the_answer_correct = %s
        ''', (id_question, responce_text, is_the_answer_correct, ))
        rows = self.cur.fetchall()
        return str(rows[0])

    # Данные о работодателе вводятся при регистрации
    def add_autor(self, full_name, company, company_address, mail, phone):
        self.cur.execute('''
        INSERT INTO Autor(full_name, company, company_address, mail, phone)
        VALUES(%s, %s, %s, %s, %s)
        ''', (full_name, company, company_address, mail, phone, ))
        self.conn.commit()

    def add_profession(self, profession, specialization, wage):
        self.cur.execute('''
        SELECT name, specialization, wage FROM Profession
        WHERE name = %s
        AND specialization = %s
        AND wage = %s
        ''', (profession, specialization, wage, ))
        rows = self.cur.fetchall()
        if len(rows) == 0:
            self.cur.execute('''
            INSERT INTO Profession(name, specialization, wage)
            VALUES(%s, %s, %s)
            ''', (profession, specialization, wage, ))
            self.conn.commit()

    def add_applicant(self, input_json):
        for i in input_json.keys():
            for key, value in input_json[i][0].items():
                if value == []:
                    input_json[i][0][key] = 'No information'
                print(''.join(value), sep='')

        for i in input_json.keys():
            full_name = ''.join(input_json[i][0]["full_name"])
            link_to_telegram = ''.join(input_json[i][0]["link_tg"])
            age = ''.join(input_json[i][0]["vozras"])
            education = ''.join(input_json[i][0]["obrazovani"])
            link_to_resume = i
            skills = ','.join(input_json[i][0]["rezum"])
            experience = ''.join(input_json[i][0]["opyt_rabot"])
            schedule = ''.join(input_json[i][0]["grafic_rabot"][0])
            employment = ''.join(input_json[i][0]["grafic_rabot"][1])
            profession = ''.join(input_json[i][0]["profesii"])
            specialization = ''.join(input_json[i][0]["spesialyzasy"])
            wage = ''.join(input_json[i][0]["zarplat"])
        
        self.add_profession(profession, specialization, wage)
        id_profession = self.get_id_profession(profession, specialization, wage)
        self.cur.execute('''
        INSERT INTO Applicant(full_name, link_to_telegram, age, education, link_to_resume, skills, experience, schedule, employment, id_profession)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (full_name, link_to_telegram, age, education, link_to_resume, skills, experience, schedule, employment, id_profession, ))
        self.conn.commit()

    def add_test(self, name, description, date_of_creation):
        self.cur.execute('''
        INSERT INTO Test(name, description, date_of_creation)
        VALUES(%s, %s, %s)
        ''', (name, description, date_of_creation, ))
        self.conn.commit()

    def add_authorship(self, id_test, id_author):
        self.cur.execute('''
        INSERT INTO Authorship(id_test, id_author)
        VALUES(%s, %s)
        ''', (id_test, id_author, ))
        self.conn.commit()

    def add_test_question(self, id_question, id_test):
        self.cur.execute('''
        INSERT INTO Test_question(id_question, id_test)
        VALUES(%s, %s)
        ''', (id_question, id_test, ))
        self.conn.commit()

    def add_question(self, number, text, correct_answer, points):
        self.cur.execute('''
        INSERT INTO Question(number, text, correct_answer, points)
        VALUES(%s, %s, %s)
        ''', (number, text, correct_answer, points, ))
        self.conn.commit()

    def add_answer(self, id_question, responce_text, is_the_answer_correct):
        self.cur.execute('''
        INSERT INTO Answer(id_question, responce_text, is_the_answer_correct)
        VALUES(%s, %s, %s)
        ''', (id_question, responce_text, is_the_answer_correct, ))
        self.conn.commit()

    def add_test_qestion_answer(self, str_test, test):
        current_datetime = datetime.now()
        current_datetime = str(current_datetime.year) + '-' + str(current_datetime.month) + '-' + str(current_datetime.day) + ' ' + str(current_datetime.hour) + ':' + str(current_datetime.minute)
        date_of_creation_test = current_datetime
        name_test = str_test["name"]
        description_test = str_test["description"]
        mail_autor = str_test["mail"]
        self.add_test(name_test, description_test, date_of_creation_test)
        self.add_authorship(self.get_id_test(name_test, description_test, date_of_creation_test), self.get_id_author(mail_autor))
        test = test["text"]
        for i in range(len(test)):
            number_question = i+1
            text_question = list(test.keys())[i]
            for j in range(len(list(test.values())[i])):
                if list(test.values())[i][j]["points"] != 0:
                    correct_answer = list(test.values())[i][j]["answer"]
                    points = list(test.values())[i][j]["points"]
            self.add_question(number_question, text_question, correct_answer, points)
            for j in range(len(list(test.values())[i])):
                answer_for_question = list(test.values())[i][j]["answer"]
                if list(test.values())[i][j]["points"] != 0:
                    is_the_answer_correct = True
                    correct_answer = list(test.values())[i][j]["answer"]
                    points = list(test.values())[i][j]["points"]
                else:
                    is_the_answer_correct = False
                self.add_answer(self.get_id_question(number_question*3 + j+1, text_question, correct_answer, points), answer_for_question, is_the_answer_correct)

    def return_data_for_bot_check(self, mail, name):
        self.cur.execute('''
        SELECT Question.text, Answer.response_text, Applicant_answers.score_for_the_answer, Test_result.id_applicant, SUM(Applicant_answers.score_for_the_answer) AS total_score
        FROM Question
        INNER JOIN Test_question ON Question.id = Test_question.id_question
        INNER JOIN Test ON Test_question.id_test = Test.id
        INNER JOIN Authorship ON Test.id = Authorship.id_test
        INNER JOIN Author ON Authorship.id_author = Author.id
        INNER JOIN Test_result ON Test.id = Test_result.id_test
        INNER JOIN Applicant ON Test_result.id_applicant = Applicant.id
        INNER JOIN Applicant_answers ON Question.id = Applicant_answers.id_question AND Test_result.id = Applicant_answers.id_result
        INNER JOIN Answer ON Question.id = Answer.id_question AND Answer.is_the_answer_correct = true
        WHERE Test.name = %s AND Author.mail = %s
        GROUP BY Question.text, Answer.response_text, Applicant_answers.score_for_the_answer, Test_result.id_applicant
        ORDER BY Test_result.id_applicant;
        ''', (name, mail, ))
        rows = self.cur.fetchall()
        print(rows)

    def return_list_applicants(self):
        pass

# ИСПОЛЬЗОВАНИЕ
# Создание БД
my_database = Main_Table()
print(my_database.return_data_for_bot_check("ivanov@mail.ru", "Test 1"))


