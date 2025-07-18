import db.sqliteDb as db
from telegram import (
    Update,
    InlineQueryResultArticle,
    InputTextMessageContent,)
from telegram.ext import (
    ContextTypes
)
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
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

async def my_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user = db.get_user_data(user_id=update.effective_chat.id)
        if user is None:
            raise ValueError("Пользователь не найден")
        answer = (
            "Ваша учетная запись успешно найдена!\n"
            "Ваши данные:\n"
            f"ID: {user[0]}\n"
            f"User Name: {user[1]}\n"
            f"First Name: {user[2]}\n"
            f"Last Name: {user[3]}\n"
            f"Full Name: {user[4]}\n"
        )
        await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)
    except Exception as ex:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Не удалось вас определить ({ex})")

async def echo_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Я не знаю, что делать с этим сообщением")

async def caps_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
    
async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        answer = (
            "Для начала введите команду /start.\n"
            "Для ответа капсом /caps.\n"
        )
        await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)
        
async def handle_invalid_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.callback_query.answer()
        await update.effective_message.edit_text(
            "Извините, я не могу обработать нажатие этой кнопки 😕 Пожалуйста, отправьте /start, чтобы получить новую клавиатуру."
        )
        
async def list_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
                reply_markup=self.build_keyboard(),
            )
            # Если используете callback_data с хранением состояния, здесь нужно реализовать логику очистки/обновления

async def unknown_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Извини, я не понимаю эту команду")            
    
    