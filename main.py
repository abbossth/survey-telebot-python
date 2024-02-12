import telebot
from telebot import types

import config

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = telebot.TeleBot(config.BOT_TOKEN)

questions = [
    "Question 1: What is your favorite programming language?",
    "Question 2: What is your favorite color?",
    "Question 3: What is your favorite food?",
    "Question 4: Where are you from?",
    "Question 5: What is your favorite animal?",
    "Question 6: Which programming languages do you know?"
]

answers = [
    ["Python", "Java", "JavaScript", "C++", "Other"],
    ["Red", "Blue", "Green", "Other"],
    ["Pizza", "Sushi", "Burgers", "Other"],
    ["North America", "Europe", "Asia", "Other"],
    ["Dog", "Cat", "Bird", "Other"],
    ["Python", "Java", "JavaScript", "C++", "Other"]
]

pressed_buttons = {}
current_question = 0


@bot.message_handler(commands=['start', 'survey'])
def send_first_question(message):
    send_question(message, current_question)


def send_question(message, question_number):
    if question_number < len(questions):
        if question_number < 5:  # Radio buttons for questions 1-5
            send_radio_question(message, questions[question_number], answers[question_number])
        else:  # Checkbox for question 6
            send_radio_question(message, questions[question_number], answers[question_number])
    else:
        bot.send_message(message.chat.id, "Thank you for completing the survey!")


def send_radio_question(message, question, options):
    markup = types.InlineKeyboardMarkup()
    for option in options:
        markup.add(types.InlineKeyboardButton(text=f"⚪️ {option}", callback_data=option))
    bot.send_message(message.chat.id, question, reply_markup=markup)


def send_checkbox_question(message, question, options):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for option in options:
        markup.add(types.KeyboardButton(text=f"⚪️ {option}"))
    bot.send_message(message.chat.id, question, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_radio_answer(call):
    text = pressed_buttons.get(call.message.text) if pressed_buttons else None
    if call.data == text:
        bot.send_message(call.message.chat.id, "Same Option")
        return print("Same")
        pass
    else:
        selected_option = call.data
        question_text = call.message.text
        pressed_buttons[question_text] = selected_option
        print(selected_option, question_text, pressed_buttons)
        # Change the symbol from ☐ to ☑ (checked) when selected
        markup = types.InlineKeyboardMarkup()
        for option in answers[questions.index(question_text)]:
            if option == selected_option:
                markup.add(types.InlineKeyboardButton(text=f"🔘 {option}", callback_data=option))
            else:
                markup.add(types.InlineKeyboardButton(text=f"⚪️ {option}", callback_data=option))

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=question_text,
                          reply_markup=markup)
        send_next_question()
        pass

@bot.message_handler(func=lambda message: True)
def handle_answer(message):
    send_next_question(message)


# def send_next_question(message):
#     for i, question in enumerate(questions):
#         if question not in pressed_buttons:
#             send_question(message, i)
#             return
#     bot.send_message(message.chat.id, "Thank you for completing the survey!")


def send_next_question(message):
    for i, question in enumerate(questions):
        if question not in pressed_buttons:
            send_question(message, current_question+1)
            return
    bot.send_message(message.chat.id, "Thank you for completing the survey!")


bot.polling()
