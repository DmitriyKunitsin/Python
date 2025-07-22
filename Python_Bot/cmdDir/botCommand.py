import db.sqliteDb as db
from configs.UserProfile import UserProfile
from configs.userData import ASK_AGE
from configs.userData import ASK_WEIGHT
from configs.userData import ASK_HEIGHT
from configs.userData import ASK_GENDER
from configs.userData import ASK_CONST_STRING_END
from configs.userData import get_state_text

from telegram import (
    Update,
    InlineQueryResultArticle,
    InputTextMessageContent,
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup
    )
from telegram.ext import (
    ContextTypes,
    ConversationHandler
)

Name_BOT_data = "UserProfile"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = context.user_data[Name_BOT_data] = UserProfile.load_foarm(update.effective_user.id)
    db.add_or_update_user(user)
    message = (
        "Привет! Я твой бот-помощник в мире фитнеса.\n"
        "Я могу быть полезен спортсменам следующим образом:\n"
        "- Отвечаю на вопросы по тренировкам и питанию\n"
        "- Помогаю отслеживать прогресс и ставить цели\n"
        "- Могу напомнить о тренировке или воде\n"
        "- Дам советы по восстановлению и мотивации\n\n"
        "Напиши команду или вопрос, чтобы начать!"
    )
    try:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    except Exception:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Не удалось обработать команду")
# --- Методы диалога сбора информации пользователя ---

async def ask_gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data[Name_BOT_data].gender = text
    db.add_or_update_user(context.user_data[Name_BOT_data])
    await update.message.reply_text(f"Спасибо! Ваш пол сохранён. Регистрация окончена")
    return ConversationHandler.END

async def ask_height(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if not text.isdigit():
        await update.message.reply_text("Bведите пожалуйста число\n Давай попробуем снова, введите свой рост")
        return ASK_HEIGHT
    height = float(text)
    if height < 50 or height > 272:
        await update.message.reply_text("Ого, но небывает таких людей, либо бегом в книгу рекордов гиннеса!!!\n Давай попробуем снова, введите свой рост")
        return ASK_HEIGHT
    context.user_data[Name_BOT_data].height = height
    # Список кнопок для ответа
    reply_keyboard = [['Boy', 'Girl']]
    # Создаем простую клавиатуру для ответа
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text(f"Спасибо! Ваш рост {height} сохранён. ")
    await update.message.reply_text(
    (
        "Выберите ваш пол , пожалуйста \n" 
        "Oтправь /cancel, если стесняешься." 
    ),
    reply_markup=markup_key,
    )
    return ASK_GENDER
"""
Запрос веса
"""
async def ask_weight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if not text.isdigit():
        await update.message.reply_text("Bведите пожалуйста число\n Давай попробуем снова, введите свой вес")
        return ASK_WEIGHT
    weight = float(text)
    if weight < 2 or weight > 635:
        await update.message.reply_text("Кажется ваши весы сломаны\n Давай попробуем снова, введите свой вес")
        return ASK_WEIGHT
    context.user_data[Name_BOT_data].weight = weight
    await update.message.reply_text(f"Спасибо! Ваш вес {weight} сохранён.")
    await update.message.reply_text(
        (
            "Введите ваш рост , пожалуйста \n" 
            "Oтправь /skip, если стесняешься." 
        ),
        reply_markup=ReplyKeyboardRemove(),
    )
    return ASK_HEIGHT

"""
Запрос возраста
"""
async def ask_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if not text.isdigit():
        await update.message.reply_text("Столько не живут, введите пожалуйста число")
        return ASK_AGE
    age = int(text)
    if age < 0 or age > 100:
        await update.message.reply_text("Не брат, столько не живут. Укажите возраст от 1 до 99.")
        return ASK_AGE
    context.user_data[Name_BOT_data].age = age
    await update.message.reply_text(f"Спасибо! Ваш возраст {age} сохранён.\n")
    # Следующее сообщение с удалением клавиатуры `ReplyKeyboardRemove`
    await update.message.reply_text(
        (
            "Введите ваш вес , пожалуйста \n" 
            "Oтправь /skip, если стесняешься." 
        ),
        reply_markup=ReplyKeyboardRemove(),
    )
    return ASK_WEIGHT


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Регистрация отменена.")
    return ConversationHandler.END
async def register_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(text="Укажите свой возраст")
    # Следующее сообщение с удалением клавиатуры `ReplyKeyboardRemove`
    await update.message.reply_text(
        'Oтправь /skip, если стесняешься.',
        reply_markup=ReplyKeyboardRemove(),
    )
    return ASK_AGE

def make_skip_handler(next_step):
    async def skip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        if get_state_text(next_step) == ASK_CONST_STRING_END:
            await update.message.reply_text(f"Регистрация окончена. \nДля получения информации о себе, введите комманду /my")
        else:
            await update.message.reply_text(f"Ладно, перейдем на следующий шаг , укажите пожалуйста {get_state_text(next_step)}")
        return next_step
    return skip

# Конец методов диалога
async def my_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_profile = UserProfile.load_foarm(update.effective_user.id)#context.user_data[Name_BOT_data]
        if user_profile is None:
            print(f'Не удалось найти пользователя {update.effective_user.username} в базе данных')
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Вас {update.effective_user.username} не удалось найти в базе данных, пройдите пожалуйста регистрацию')
            return
        answer = (
            "Ваша учетная запись успешно найдена!\n"
            "Ваши данные:\n"
            f"ID: {user_profile.id}\n"
            f"User Name: {context.bot_data[Name_BOT_data].username}\n"
            f"First Name: {user_profile.first_name}\n"
            f"Last Name: {user_profile.last_name}\n"
            f"Full Name: {user_profile.full_name}\n"
            f"premium : {user_profile.get_is_premium()}\n"
            f"Рост : {user_profile.height}\n"
            f"Вес : {user_profile.weight}\n"
            f"ИМТ : {user_profile.calc_iwm()} ({user_profile.get_stadia_iwm()})\n"
            f"Пол : {user_profile.gender}\n"
            f"Возраст : {user_profile.age}\n"
            f"почта : {user_profile.email}\n"
            f"дата регистрации : {user_profile.register_date}\n"
        )
        await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)
    except ValueError as ex:
        print(ex)
    except FileNotFoundError as ex:
        print(ex)
    except RuntimeError as ex:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Не удалось вас определить ({ex})")

async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Я не знаю, что делать с этим сообщением")

async def caps_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        text_caps = " ".join(context.args).upper()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def inline_caps(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        from uuid import uuid4

        query = update.inline_query.query
        if not query:
            return
        results = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="Caps",
                input_message_content=InputTextMessageContent(message_text=query.upper()),
            )
        ]
        await context.bot.answer_inline_query(update.inline_query.id, results)
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        answer = (
            "Для начала введите команду /start.\n"
            "Для начала регистрации /reg.\n"
            "Для получения сохраненной информации о себе /my. \n"
        )
        await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)
        
async def handle_invalid_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.callback_query.answer()
        await update.effective_message.edit_text(
            "Извините, я не могу обработать нажатие этой кнопки 😕 Пожалуйста, отправьте /start, чтобы получить новую клавиатуру."
        )
        
async def list_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()
        # Пример: ожидаем, что callback_data — строка с двумя числами, разделёнными запятой, например "3,[1,2]"
        try:
            # Пример парсинга: в вашем коде это нужно адаптировать под формат callback_data
            data_str = query.data  # строка
            # Если callback_data — сериализованный список, нужно десериализовать (например, через json.loads)
            # Здесь пример простой обработки, нужно подстроить под реальный формат
            number = int(data_str)  # если это просто число
            number_list = []  # или получить из контекста, если есть
        except Exception:
            number = None
            number_list = []

        if number is not None:
            number_list.append(number)
            await query.edit_message_text(
                text=f"Вы выбрали: {number_list}. Выберите следующий элемент:",
            )
            # Если используете callback_data с хранением состояния, здесь нужно реализовать логику очистки/обновления

async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Извини, я не понимаю эту команду")            
    
    