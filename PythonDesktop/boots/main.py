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
        btn1 = types.KeyboardButton('Как стать автором на Хабре?')
        btn2 = types.KeyboardButton('Правила сайта')
        btn3 = types.KeyboardButton('Советы по оформлению публикации')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.from_user.id, '❓ Задайте интересующий вопрос', reply_markup= markup)#ответ бота
    elif message.text == 'Как стать автором на Хабре?':
        bot.send_message(message.from_user.id, 'Вы пишете первый пост, его проверяют модераторы, и, если всё хорошо, отправляют в основную ленту Хабра, где он набирает просмотры, комментарии и рейтинг. В дальнейшем премодерация уже не понадобится. Если с постом что-то не так, вас попросят его доработать.\n \nПолный текст можно прочитать по ' + '[ссылке](https://habr.com/ru/sandbox/start/)', parse_mode='Markdown')
    elif message.text == 'Правила сайта':
        bot.send_message(message.from_user.id, 'Прочитать правила сайта вы можете по ' + '[ссылке](https://habr.com/ru/docs/help/rules/)', parse_mode='Markdown')
    elif message.text == 'Советы по оформлению публикации':
        # чтобы сделать гиперссылку мы берем в квадратные скобки слово, которое будет ссылкой, а саму ссылку берем в круглые
        bot.send_message(message.from_user.id, 'Подробно про советы по оформлению публикаций прочитать по ' + '[ссылке](https://habr.com/ru/docs/companies/design/)', parse_mode='Markdown')

bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть