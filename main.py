import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import answers
import db

bot = telebot.TeleBot("8572737959:AAFSxwZJ6ftj4bjzfaP7_YfXC8DY4qxToGw")

@bot.message_handler(commands=['start'])
def start(m):
    markup = InlineKeyboardMarkup()
    b1 = InlineKeyboardButton(answers.buttons["help"], callback_data='help')
    b2 = InlineKeyboardButton(answers.buttons["proghelp"], callback_data='proghelp')
    markup.row(b1)
    markup.row(b2)
    bot.send_message(m.chat.id, answers.start_message, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'help':
        bot.send_message(call.message.chat.id, "Пожалуйста, задайте ваш вопрос.")
    elif call.data == 'proghelp':
        bot.send_message(call.message.chat.id, "Пожалуйста, опишите проблему с сайтом и мы постараемся ее решить.")

bot.polling(none_stop=True)