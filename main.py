import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
import answers
import db
import ii
import json

bot = telebot.TeleBot("")

com = []
for command in answers.commands.keys():
    com.append(BotCommand(command, answers.commands[command]))
print(com)
bot.set_my_commands(com)

@bot.message_handler(commands=['start'])
def start(m):
    markup = InlineKeyboardMarkup()
    b1 = InlineKeyboardButton(answers.buttons["help"], callback_data='help')
    b2 = InlineKeyboardButton(answers.buttons["proghelp"], callback_data='proghelp')
    b3 = InlineKeyboardButton(answers.buttons["myask"], callback_data='myask')
    markup.row(b1)
    markup.row(b2)
    markup.row(b3)
    bot.send_message(m.chat.id, answers.start_message, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'help':
        bot.send_message(call.message.chat.id, "Пожалуйста, задайте ваш вопрос.")
        bot.register_next_step_handler(call.message, process_help)
    elif call.data == 'proghelp':
        bot.send_message(call.message.chat.id, "Пожалуйста, опишите проблему с сайтом и мы постараемся ее решить.")
        bot.register_next_step_handler(call.message, process_bug)

    elif call.data == 'changebut':
        mar = InlineKeyboardMarkup()
        for i in answers.buttons:
            mar.row(InlineKeyboardButton(callback_data=i + "change", text=answers.buttons[i]))
        bot.send_message(call.message.chat.id, "Выберите кнопку для изменения текста", reply_markup=mar)

    elif call.data.replace("change", "") in answers.buttons.keys():
        msg = bot.send_message(call.message.chat.id, "Введите новый текст для кнопки")
        bot.register_next_step_handler(msg, change_but, call.data.replace("change", ""))

    elif call.data == 'changehi':
        msg = bot.send_message(call.message.chat.id, "Введите новый приветственный текст")
        bot.register_next_step_handler(msg, change_hi)

    elif call.data == 'changeans':
        mar = InlineKeyboardMarkup()
        for i in answers.answers:
            mar.row(InlineKeyboardButton(callback_data=i + "changeans", text=answers.answers[i]))
        bot.send_message(call.message.chat.id, "Выберите ответ для изменения текста", reply_markup=mar)
    
    elif call.data.replace("changeans", "") in answers.answers.keys():
        msg = bot.send_message(call.message.chat.id, "Введите новый текст для ответа")
        bot.register_next_step_handler(msg, change_ans, call.data.replace("changeans", ""))

    elif call.data == 'changecom':
        mar = InlineKeyboardMarkup()
        for i in answers.commands:
            mar.row(InlineKeyboardButton(callback_data=i, text=answers.commands[i]))
        bot.send_message(call.message.chat.id, "Выберите команду для изменения текста", reply_markup=mar)

    elif call.data in answers.commands.keys():
        msg = bot.send_message(call.message.chat.id, "Введите новый текст для команды")
        bot.register_next_step_handler(msg, change_com, call.data)

def change_com(message, com):
    answers.commands[com] = message.text
    for command in answers.commands:
        bot.set_my_commands([telebot.types.BotCommand(command, answers.commands[command])])
    bot.send_message(message.chat.id, "Текст команды изменен.")

def change_ans(message, ans):
    answers.answers[ans] = message.text
    bot.send_message(message.chat.id, "Текст ответа изменен.")

    

def change_hi(message):
    answers.start_message = message.text
    bot.send_message(message.chat.id, "Приветственное сообщение изменено.")

def change_but(message, but):
    answers.buttons[but] = message.text
    bot.send_message(message.chat.id, "Текст кнопки изменен.")

def process_help(message):
    db.add_help(message.chat.id, message.text)
    if ii.resp(message.text) in answers.answers:
        bot.send_message(message.chat.id, answers.answers[ii.resp(message.text)])
        return
    bot.send_message(message.chat.id, "Спасибо за ваш вопрос, мы постараемся ответить на него как можно скорее.")

def process_bug(message):
    db.add_bug(message.chat.id, message.text)
    bot.send_message(message.chat.id, "Спасибо за сообщение о баге, мы постараемся решить эту проблему как можно скорее.")

@bot.message_handler(commands=['setadmin'])
def set_admin(m):
    try:
        admins = db.get_admins()
        m.text = m.text.split()
        if m.text[1] in admins:
            bot.send_message(m.chat.id, "Пользователь уже является администратором.")
        else:
            m.text[1] = m.text[1].replace('@', '')
            db.add_admin(m.text[1])
            bot.send_message(m.chat.id, "Пользователь добавлен в список администраторов.")
    except Exception as e:
        bot.send_message(m.chat.id, "Пожалуйста, укажите имя пользователя после команды. Например: /setadmin @username ")
        bot.send_message(m.chat.id, "Ошибка: " + str(e))
    
@bot.message_handler(commands=["admin"])
def admin_panel(m):
    admins = db.get_admins()
    print(admins)
    print(m.chat.username)
    if m.chat.username in str(admins):
        mar = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton("Изменить текст кнопок", callback_data='changebut')
        b2 = InlineKeyboardButton("Изменить приветсвеное сообщение", callback_data='changehi')
        b3 = InlineKeyboardButton("Изменить ответы на вопросы", callback_data='changeans')
        b4 = InlineKeyboardButton("Изменить список команд", callback_data='changecom')
        mar.row(b1)
        mar.row(b2)
        mar.row(b3)
        mar.row(b4)
        bot.send_message(m.chat.id, "Панель администратора", reply_markup=mar)
    else:
        bot.send_message(m.chat.id, "У вас нет доступа к этой команде.")

bot.polling(none_stop=True)