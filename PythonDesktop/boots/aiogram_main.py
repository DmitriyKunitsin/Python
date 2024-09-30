import aiogram
import asyncio  # Импортируйте asyncio
print(aiogram.__version__)
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.fsm import FSMContext
from aiogram.types import ParseMode
from token_bot import Token

# Инициализация бота и диспетчера
bot = Bot(Token.token)
dp = Dispatcher()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    await message.answer("👋 Привет! Я твой бот-помошник!", reply_markup=markup)

@dp.message_handler(lambda message: message.text == "👋 Поздороваться")
async def greet_user(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Как стать автором на Хабре?')
    btn2 = types.KeyboardButton('Правила сайта')
    btn3 = types.KeyboardButton('Советы по оформлению публикации')
    markup.add(btn1, btn2, btn3)
    await message.answer('❓ Задайте интересующий вопрос', reply_markup=markup)

@dp.message_handler(lambda message: message.text == 'Как стать автором на Хабре?')
async def become_author(message: types.Message):
    await message.answer('Вы пишете первый пост, его проверяют модераторы, и, если всё хорошо, отправляют в основную ленту Хабра, где он набирает просмотры, комментарии и рейтинг. В дальнейшем премодерация уже не понадобится. Если с постом что-то не так, вас попросят его доработать.\n\nПолный текст можно прочитать по ссылке', parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(lambda message: message.text == 'Правила сайта')
async def site_rules(message: types.Message):
    await message.answer('Прочитать правила сайта вы можете по ссылке', parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(lambda message: message.text == 'Советы по оформлению публикации')
async def publication_tips(message: types.Message):
    await message.answer('Подробно про советы по оформлению публикаций прочитать по ссылке', parse_mode=ParseMode.MARKDOWN)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':  # Исправлено условие
    asyncio.run(main())
