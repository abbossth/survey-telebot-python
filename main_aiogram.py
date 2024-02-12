import telebot
from telebot import types
import config
from data import print_doc

# Replace 'YOUR_BOT_TOKEN' with your actual bot token obtained from BotFather
bot = telebot.TeleBot(config.BOT_TOKEN)

# Define the survey questions
questions = [
    {
        "number": 1,
        "question": "ruWhat is your favorite color?",
        "answers": ["Red", "Green", "Blue"]
    },
    {
        "number": 2,
        "question": "ruWhich of the following animals do you like?",
        "answers": ["Dog", "Cat", "Bird", "Fish"]
    },
    {
        "number": 3,
        "question": "ru33What is your favorite color?",
        "answers": ["Red", "Green", "Blue"]
    },
    {
        "number": 4,
        "question": "ru44What is your favorite color?",
        "answers": ["Red", "Green", "Blue"]
    },
    {
        "number": 5,
        "question": "ru55What is your favorite color?",
        "answers": ["Red", "Green", "Blue"]
    },
]

# Define the survey questions
questions_uz = [
    {
        "number": 1,
        "question": "uzWhat is your favorite color?",
        "answers": ["Red", "Green", "Blue"]
    },
    {
        "number": 2,
        "question": "uzWhich of the following animals do you like?",
        "answers": ["Dog", "Cat", "Bird", "Fish"]
    },
    {
        "number": 3,
        "question": "Yes or No?",
        "answers": ["Yes", "No"]
    },
    {
        "number": 4,
        "question": "uz44What is your favorite color?",
        "answers": ["Red", "Green", "Blue"]
    },
    {
        "number": 5,
        "question": "uz55What is your favorite color?",
        "answers": ["Red", "Green", "Blue"]
    },
]

# bot languages
languages = [{"code": "uz", "text": "Узбек Тили"}, {"code": "ru", "text": "Русский Язык"}]

# chosen language || by default it is *ru*
lang = "ru"

# Keep track of user answers
user_answers = {}

# Keep track of question length
user_question_length = {}

# Keep track of the current question for each user
user_current_question = {}


# Helper function to generate inline keyboard markup
def generate_markup(question, answers):
    markup = types.InlineKeyboardMarkup()
    for answer in answers:
        markup.add(types.InlineKeyboardButton(text=f"⚪️ {answer}", callback_data=f"{question}_{answer}"))
    return markup


def generate_markup_languages():
    markup = types.InlineKeyboardMarkup(row_width=2)
    for answer in languages:
        markup.add(types.InlineKeyboardButton(text=f"{answer["text"]}", callback_data=f"{answer["code"]}"))
    return markup


# Handler for start command
@bot.message_handler(commands=['start', 'survey'])
def handle_start(message):
    bot.send_message(message.chat.id, "Welcome to the Survey Bot! Let's get started with the survey.", reply_markup=generate_markup_languages())
    user_current_question[message.chat.id] = 0  # Set the current question to the first question
    user_answers[message.chat.id] = {}
    user_question_length[message.chat.id] = len(questions)


# Send survey question
def send_question(chat_id):
    print("*****************")
    current_question = user_current_question[chat_id]
    # print("curr: ", current_question)
    # print("ua: ", user_answers)
    number = user_answers[chat_id].get(2) if user_answers else None
    value = next(iter(number)) if number else None
    # print(value)
    if value == "No" and user_current_question[chat_id] == 3:
        if int(3) not in user_answers:
            user_answers[chat_id][int(3)] = set()
        user_answers[chat_id][3].add("-")
        user_current_question[chat_id] = 4
        current_question = user_current_question[chat_id]
        # user_question_length[chat_id] -= 1
    print("len: ", user_question_length)
    print("curr: ", current_question)
    print(user_current_question[chat_id])
    if lang == "uz":
        if current_question < user_question_length[chat_id]:
            question = questions_uz[current_question]
            return bot.send_message(chat_id, f"Question {question['number']}: {question['question']}", reply_markup=generate_markup(current_question, question["answers"]))
        else:
            return bot.send_message(chat_id, f"Thank you very much!")
    elif lang == "ru":
        if current_question < user_question_length[chat_id]:
            question = questions[current_question]
            return bot.send_message(chat_id, f"Question {question['number']}: {question['question']}", reply_markup=generate_markup(current_question, question["answers"]))
        else:
            return bot.send_message(chat_id, f"Thank you very much!")


# Handler for inline keyboard button clicks
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    global lang
    curr = user_current_question.get(call.message.chat.id) if user_current_question else None
    if curr != 0 and curr is not None:
        pass
    else:
        user_current_question[call.message.chat.id] = 0  # Set the current question to the first question
    # print(curr)
    # print(user_current_question[call.message.chat.id])
    # print("s: ", call.data)
    if call.data == "selected":
        return
    if call.data == "ru":
        lang = 'ru'
        print_doc()
        return send_question(call.message.chat.id)
    if call.data == "uz":
        lang = 'uz'
        return send_question(call.message.chat.id)
    question_idx, answer = call.data.split('_')
    chat_id = call.message.chat.id

    # Update user_answers dictionary
    if int(question_idx) not in user_answers[chat_id]:
        user_answers[chat_id][int(question_idx)] = set()
    answers = user_answers[chat_id][int(question_idx)]
    answers.clear()
    answers.add(answer)
    # print(answers)
    # print(user_answers)
    # print(answer)
    # print(question_idx)

    if answer != user_answers.get(question_idx):
        # Change the button state from ⚪️ to 🔘
        if lang == "ru":
            markup = generate_markup(question_idx, questions[int(question_idx)]["answers"])
            for row in markup.keyboard:
                for button in row:
                    if button.callback_data == call.data:
                        button.text = f"🔘 {answer}"
                        button.callback_data = "selected"
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)
        elif lang == "uz":
            markup = generate_markup(question_idx, questions_uz[int(question_idx)]["answers"])
            for row in markup.keyboard:
                for button in row:
                    if button.callback_data == call.data:
                        button.text = f"🔘 {answer}"
                        button.callback_data = "selected"
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)
    idx = int(question_idx) if question_idx else None
    curr_question = int(user_current_question.get(chat_id)) if user_current_question else None
    # print(user_answers)
    # Update the current question for the user
    if idx == curr_question:
        # print(True)
        user_current_question[chat_id] += 1
        # Send next question if available, else end survey
        send_question(chat_id)
    return


# Start the bot
bot.polling()