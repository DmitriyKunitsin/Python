import telebot
from telebot import types # Кнопки
from token_bot import Token

bot = telebot.TeleBot(Token.token)
# # Inline-кнопки
# @bot.message_handler(commands=['Start'])
# def url(message):
#     markup = types.InlineKeyboardMarkup()
#     btn1 = types.InlineKeyboardButton(text='Наш сайт', url='https://habr.com/ru/all/')
#     markup.add(btn1)
#     bot.send_message(message.from_user.id, 'По кнопке ниже можно перейти на сайт хабра', reply_markup= markup)
    
# # Keyboard-кнопки
# @bot.message_handler(commands=['start'])
# def strart(message):

#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     btn1 = types.KeyboardButton("Русский")
#     btn2 = types.KeyboardButton("Английский")
#     markup.add(btn1, btn2)
#     bot.send_message(message.from_user.id, "🇷🇺 Выберите язык / 🇬🇧 Choose your language", reply_markup=markup)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Привет! Я твой бот-помошник!", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if message.text == '👋 Поздороваться':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) # создание новых кнопок