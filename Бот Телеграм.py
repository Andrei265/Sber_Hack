import telebot
import config
import database_module

bot = telebot.TeleBot(config.token_test)

test_data = {}
questions = []
test_vict = {}
test_vink = {}
# функция, которая будет запускаться при /start
@bot.message_handler(commands=['start'])
def start_command(message):
    chat_id = message.chat.id

    # запрос на ввод названия теста
    msg = bot.send_message(chat_id, "Введите название теста:")
    bot.register_next_step_handler(msg, get_test_name)


# функция для получения названия теста
def get_test_name(message):
    chat_id = message.chat.id
    test_data['name'] = message.text

    # запрос на ввод описания теста
    msq = bot.send_message(chat_id, "Введите описание теста:")
    bot.register_next_step_handler(msq, get_test_description)


# функция для получения описания теста
def get_test_description(message):
    chat_id = message.chat.id
    test_data['description'] = message.text

    msq = bot.send_message(chat_id, "Введите вашу электронную почту:")
    bot.register_next_step_handler(msq, get_test_mail)


def get_test_mail(message):
    chat_id = message.chat.id
    test_data['mail'] = message.text
    msq = bot.send_message(chat_id, "Отлично, данные теста успешно сохранены, введите вопрос для теста")
    print(test_data)
    bot.register_next_step_handler(msq, get_questions)


def get_questions(message):
    chat_id = message.chat.id
    question = message.text
    test_vict[question] = []

    # запрашиваем ответы на вопрос
    msq = bot.send_message(chat_id, f"Введите три варианта ответа на вопрос '{question}' в одном сообщении, разделяя их переносом строки и указывая через запятую количество баллов за ответ:")
    bot.register_next_step_handler(msq, get_answers, question)


def get_answers(message, question):
    chat_id = message.chat.id
    answers = message.text.split('\n')

    # проверяем, что количество ответов соответствует требуемому (3)
    if len(answers) == 3:
        for answer in answers:
            answer_data = answer.split(',')
            if len(answer_data) == 2:
                answer_text = answer_data[0].strip()
                answer_score = int(answer_data[1].strip())
                answer_dict = {'answer': answer_text, 'points': answer_score}
                test_vict[question].append(answer_dict)
            else:
                msq = bot.send_message(chat_id,
                                       f"Вы ввели некорректный ответ ({answer}). Введите все варианты ответа на вопрос '{question}' еще раз, разделяя их переносом строки и указывая через запятую количество баллов за ответ:")
                bot.register_next_step_handler(msq, get_answers, question)
                return

        # добавляем вопрос в список вопросов и проверяем, не добавлены ли все нужные вопросы
        questions.append(question)
        if len(questions) < 10:
            # запрашиваем следующий вопрос
            msq = bot.send_message(chat_id, "Введите следующий вопрос:")
            bot.register_next_step_handler(msq, get_questions)
        else:
            # все вопросы получены, выводим результаты и сохраняем данные теста
            msq = bot.send_message(chat_id, "Спасибо, все вопросы получены.")
            test_vink['text'] = test_vict
            print(test_vink)
            my_database = database_module.Main_Table()
            msq = bot.send_message(chat_id,
                                       my_database.return_data_for_bot_check("mark@johnsonconsulting.com", "Math Test"))
            bot.register_next_step_handler(msq, get_questions)
            my_database.close_connection()
    else:
        msq = bot.send_message(chat_id,
                               f"Вы ввели некорректное количество ответов ({len(answers)}). Введите все варианты ответа на вопрос '{question}' еще раз, разделяя их переносом строки и указывая через запятую количество баллов за ответ:")
        bot.register_next_step_handler(msq, get_answers, question)


bot.polling(none_stop=True)