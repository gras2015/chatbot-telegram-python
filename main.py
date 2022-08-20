import telebot
from telebot import types
bot = telebot.TeleBot("5440445076:AAEotg-Wgisf2lBR5vc68L3SB40GCT6aOl4")

name = ''
surname = ''
age = 0

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text =='Bonjour':
        bot.reply_to(message, 'Bonjour! Je suis un bot')
    elif message.text == 'hi':
        bot.reply_to(message, 'Hi! I am a bot')
    elif message.text == '/registration':
        bot.send_message(message.from_user.id, "Hello! What's you name?")
        bot.register_next_step_handler(message, reg_name)
   # bot.reply_to(message, message.text)


def reg_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, "What's your surname?")
    bot.register_next_step_handler(message, reg_surname)

def reg_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, "How old are you?")
    bot.register_next_step_handler(message, reg_age)

def reg_age(message):
    global age
    #age = message.text
    while age == 0:
        try:
            age = int(message.text)
        except Exception:
            bot.send_message(message.from_user.id, "Enter numbers!")

    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Yes', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='No', callback_data='no')
    keyboard.add(key_no)
    question = 'You are ' + str(age) + ' years old? And your name: ' + name + ' ' + surname + '?'
    bot.send_message(message.from_user.id, text = question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, "Nice to meet you! I will save it")
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Let's try again!")
        bot.send_message(call.message.chat.id, "Hello! What's your name?")
        bot.register_next_step_handler(call.message, reg_name)

bot.polling()