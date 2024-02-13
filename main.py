import telebot
from telebot import types
import config
from data import questions, questions_uz

# Replace 'YOUR_BOT_TOKEN' with your actual bot token obtained from BotFather
bot = telebot.TeleBot(config.BOT_TOKEN)

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
    select_symbol = "⚪️"
    if int(question) == 11:
        # select_symbol = "☐"
        select_symbol = "◻️"

    markup = types.InlineKeyboardMarkup()
    for answer in answers:
        markup.add(types.InlineKeyboardButton(text=f"{select_symbol} {answer}", callback_data=f"{question}_{answer}_none"))
    return markup


# Helper function to generate inline keyboard markup
def generate_markup_languages():
    markup = types.InlineKeyboardMarkup(row_width=2)
    for answer in languages:
        markup.add(types.InlineKeyboardButton(text=f"{answer["text"]}", callback_data=f"{answer["code"]}"))
    return markup


# finish
def send_survey_finish_message(chat_id):
    return bot.send_message(chat_id, f"Thank you very much!")


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
    # print(user_answers[chat_id])
    current_question = user_current_question[chat_id]

    # Q1
    q1_answer = user_answers[chat_id].get(0) if user_answers else None
    q1_value = next(iter(q1_answer)) if q1_answer else None
    if q1_value == "1" and current_question == 1:
        q = 1
        user_current_question[chat_id] += 7
        if int(q) not in user_answers:
            user_answers[chat_id][int(q)] = set()
        user_answers[chat_id][q].add("-")

    # Q4
    q4_answer = user_answers[chat_id].get(7) if user_answers else None
    q4_value = next(iter(q4_answer)) if q4_answer else None
    if q4_value == "нет" and current_question == 8:
        q = 8
        user_current_question[chat_id] += 1
        if int(q) not in user_answers:
            user_answers[chat_id][int(q)] = set()
        user_answers[chat_id][q].add("-")

    # Q7
    q7_answer = user_answers[chat_id].get(10) if user_answers else None
    q7_value = next(iter(q7_answer)) if q7_answer else None
    if q7_value == "нет" and current_question == 11:
        return send_survey_finish_message(chat_id)

    # Q-NEXT
    # q_next_answer = user_answers[chat_id].get(12) if user_answers else None
    # q_next_value = next(iter(q_next_answer)) if q_next_answer else None
    # if q_next_value == "нет" and current_question == 11:
    #     return send_survey_finish_message(chat_id)

    if lang == "uz":
        if current_question < user_question_length[chat_id]:
            question = questions_uz[current_question]
            return bot.send_message(chat_id, f"Question {question['number']}: {question['question']}", reply_markup=generate_markup(current_question, question["answers"]))
        else:
            send_survey_finish_message(chat_id)
    elif lang == "ru":
        if current_question < user_question_length[chat_id]:
            question = questions[current_question]
            # print(question)
            if question["has_sub_question"]:
                bot.send_message(chat_id, f"{question['question']}")
                user_current_question[chat_id] += 1
                current_question = user_current_question[chat_id]
                question = questions[current_question]
                return bot.send_message(chat_id, f"Question {question['number']}: {question['question']}",
                                 reply_markup=generate_markup(current_question, question["answers"]))
            else:
                current_question = user_current_question[chat_id]
                question = questions[current_question]
                return bot.send_message(chat_id, f"Question {question['number']}: {question['question']}", reply_markup=generate_markup(current_question, question["answers"]))
        else:
            return send_survey_finish_message(chat_id)


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
    if call.data == "ru":
        lang = 'ru'
        return send_question(call.message.chat.id)
    if call.data == "uz":
        lang = 'uz'
        return send_question(call.message.chat.id)
    if call.data == "12_next":
        return send_question(call.message.chat.id)

    question_idx, answer, select = call.data.split('_')
    chat_id = call.message.chat.id
    print("select: ", select)
    if select == "selected":
        if int(question_idx) == 11:
            user_answers[chat_id][int(question_idx)].remove(answer)
            print("Clicked checked option!")
            print(user_answers[chat_id])
        else:
            return
    # Update user_answers dictionary
    if select != "selected" and int(question_idx) not in user_answers[chat_id]:
        user_answers[chat_id][int(question_idx)] = set()
    answers = user_answers[chat_id][int(question_idx)]
    print(user_current_question[chat_id])

    if user_current_question[chat_id] != 12:  # this should be 11 after putting next button
        answers.clear()

    if select != "selected":
        answers.add(answer)

    selected_symbol = "🔘"

    if int(question_idx) == 11:
        # selected_symbol = "☑"
        selected_symbol = "☑️"

    print(user_answers[chat_id])
    print("answer: ", answer)
    print("user answer: ", user_answers[chat_id][int(question_idx)])
    if answer != user_answers.get(question_idx):
        # Change the button state from ⚪️ to 🔘
        if lang == "ru":
            # print("q: ", question_idx)
            markup = generate_markup(question_idx, questions[int(question_idx)]["answers"])
            # print("Markup: ", markup)
            for row in markup.keyboard:
                # print("row: ", row)
                for button in row:
                    btn_idx, a, select = button.callback_data.split('_')
                    print("btn: ", button.callback_data)
                    print("ua: ", user_answers[chat_id][int(question_idx)])
                    if a in user_answers[chat_id][int(question_idx)]:
                        button.text = f"{selected_symbol} {a}"
                        button.callback_data = f"{btn_idx}_{a}_selected"
                    # if button.callback_data == call.data:
                    #     button.text = f"{selected_symbol} {answer}"
                    #     button.callback_data = "selected"
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)
        elif lang == "uz":
            markup = generate_markup(question_idx, questions_uz[int(question_idx)]["answers"])
            for row in markup.keyboard:
                for button in row:
                    if button.callback_data == call.data:
                        button.text = f"{selected_symbol} {answer}"
                        button.callback_data = f"{question_idx}_selected"
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)
    idx = int(question_idx) if question_idx else None
    curr_question = int(user_current_question.get(chat_id)) if user_current_question else None
    # Update the current question for the user
    if idx == curr_question:
        # print(True)
        if idx == 10:
            user_current_question[chat_id] += 1
            # Send next question if available, else end survey
            send_question(chat_id)
            user_current_question[chat_id] += 1
            send_question(chat_id)
        else:
            user_current_question[chat_id] += 1
            # Send next question if available, else end survey
            send_question(chat_id)
    return


# Start the bot
bot.polling()
