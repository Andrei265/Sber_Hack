import telebot
from telebot import types
import config

bot = telebot.TeleBot(config.token_summ)
k = []
questions = [
    {
        "text": "Вопрос 1: Когда необходимо составлять блок-схему программы?",
        "answers": [
            {"text": "До начала составления самой программы", "points": 1},
            {"text": "В процессе составления программы", "points": 0},
            {"text": "После составления программы", "points": 0}
        ]
    },
    {
        "text": "Вопрос 2: Наиболее наглядной формой описания алгоритма является:",
        "answers": [
            {"text": "словесное описание алгоритма", "points": 0},
            {"text": "представление алгоритма в виде схемы", "points": 1},
            {"text": "язык программирования высокого уровня", "points": 0}
        ]
    },
    {
        "text": "Вопрос 3: Какой инструмент переводит программы с языка высокого уровня на язык более низкого уровня?",
        "answers": [
            {"text": "Паскаль", "points": 0},
            {"text": "Ассемблер", "points": 0},
            {"text": "Компилятор", "points": 1}
        ]
    },
    {
        "text": "Вопрос 4: Необходимо ли рисовать стрелки на линиях потоков в графических схемах алгоритмов?",
        "answers": [
            {"text": "Да, если направление потока снизу вверх и справа налево", "points": 1},
            {"text": "Можно рисовать или не рисовать", "points": 0},
            {"text": "Нет, рисовать не нужно", "points": 0}
        ]
    }
]

users = {}
otvety = ''
@bot.callback_query_handler(func=lambda call: True)
def handle_answer(call):
    global otvety
    user_id = call.from_user.id
    username = call.from_user.username
    question_index = users[user_id]["current_question"]
    question = questions[question_index]
    answer_text = call.data

    for answer in question["answers"]:
        if answer_text == str(answer["points"]):
            otvety+=(str(answer["points"]))
            users[user_id]["score"] = users[user_id].get("score", 0) + answer["points"]
            break
    users[user_id]["current_question"] += 1

    if users[user_id]["current_question"] < len(questions):
        send_question(call.message.chat.id, user_id, call.message.message_id)
    else:
        score = users[user_id]["score"]
        bot.send_message(
            call.message.chat.id, f'Пользователь {username} - {score}/{len(questions)}')
        print(otvety)
        del users[user_id]
def send_question(chat_id, user_id, message_id=None):
    question_index = users[user_id]["current_question"]
    question = questions[question_index]
    text = question["text"]
    answers = question["answers"]

    markup = types.InlineKeyboardMarkup()
    for i, answer in enumerate(answers):
        button = types.InlineKeyboardButton(answer["text"], callback_data=str(answer["points"]))
        markup.add(button)

    if message_id:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=markup)
    else:
        bot.send_message(chat_id, text, reply_markup=markup)

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    users[user_id] = {"score": 0, "current_question": 0}
    send_question(message.chat.id, user_id)
bot.polling(none_stop=True)
#[tg_link, author_mail, name_test, (ответ1, ответ3, ответ2, ответ1, ответ2)]