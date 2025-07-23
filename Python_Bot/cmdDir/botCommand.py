import db.sqliteDb as db
from configs.UserProfile import UserProfile
from configs.userData import ASK_AGE
from configs.userData import ASK_WEIGHT
from configs.userData import ASK_HEIGHT
from configs.userData import ASK_GENDER
from configs.userData import ASK_CONST_STRING_END
from configs.userData import get_state_text

NAME_CONST_CURRENT_STATE_DIALOG = "current_state_dialog"

from telegram import (
    Update,
    InlineQueryResultArticle,
    InputTextMessageContent,
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup
    )
from telegram.ext import (
    ContextTypes,
    ConversationHandler
)

Name_BOT_data = "UserProfile"

def build_button_menu(buttons, n_cols,header_buttons=None,footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = context.user_data[Name_BOT_data] = UserProfile.load_foarm(update.effective_user.id)
    if user is None:
        print(f'Пользователь {update.effective_user.username} не был найден в базе данных')
        user = context.user_data[Name_BOT_data] = UserProfile.init_user(new_user= update.effective_user)
        if user is None:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Ой, что-то пошло не так🤔. \nСообщите о возникшей проблеме разработчику 💕")
            await help_command(update=update, context=context)
            return
    db.add_or_update_user(user)
    message = (
        "Привет! Я твой бот-помощник в мире фитнеса.\n"
        "Я могу быть полезен спортсменам следующим образом:\n"
        "- Отвечаю на вопросы по тренировкам и питанию\n"
        "- Помогаю отслеживать прогресс и ставить цели\n"
        "- Могу напомнить о тренировке или воде\n"
        "- Дам советы по восстановлению и мотивации\n\n"
        "Напиши команду или пройди регистрацию, чтобы начать!\n"
        "/help для справки"
    )
    try:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    except Exception as ex:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Не удалось обработать команду")
        print(f"Произошла ошибка в методе start_command с текстом : {ex} ")
#region --- Методы диалога сбора информации пользователя ---
def creat_markup_registration_menu():
    button_list = [
        InlineKeyboardButton("Отмена", callback_data="/cancel"),
        InlineKeyboardButton("Пропустить", callback_data="/skip")
    ]
    reply_markup = InlineKeyboardMarkup(build_button_menu(button_list, n_cols=2))
    return reply_markup

async def button_handler_registration_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    print(f'Была нажата кнопка {query.data}')
    if query.data == "/cancel":
        await query.edit_message_text(text="Регистрация отменена.")
        return ConversationHandler.END
    if query.data == "/skip":
        current_state = context.user_data[NAME_CONST_CURRENT_STATE_DIALOG]
        handler = make_skip_handler(current_state)
        if current_state + 1 < 3:
            current_state += 1
        else:
            current_state = ConversationHandler.END
        context.user_data[NAME_CONST_CURRENT_STATE_DIALOG]  = current_state  
        return await handler(update, context)
    
    
async def ask_gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        text = update.message.text
        context.user_data[Name_BOT_data].gender = text
        db.add_or_update_user(context.user_data[Name_BOT_data])
        await update.message.reply_text(f"Спасибо! Ваш пол сохранён. Регистрация окончена",
                                        reply_markup=ReplyKeyboardRemove())
        await help_command(update=update, context=context)
        context.user_data[NAME_CONST_CURRENT_STATE_DIALOG] = ConversationHandler.END
        return ConversationHandler.END
    except Exception as ex:
        print(f'Метод ask_gender, произошла ошибка с текстом : {ex}')
        return ConversationHandler.END

async def ask_height(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        text = update.message.text
        if not text.isdigit():
            markup = creat_markup_registration_menu()
            await update.message.reply_text("Bведите пожалуйста число\n Давай попробуем снова, введите свой рост", reply_markup=markup)
            context.user_data[NAME_CONST_CURRENT_STATE_DIALOG] = ASK_GENDER
            return ASK_HEIGHT
        height = float(text)
        if height < 50 or height > 272:
            markup = creat_markup_registration_menu()
            await update.message.reply_text("Ого, но небывает таких людей, либо бегом в книгу рекордов гиннеса!!!\n Давай попробуем снова, введите свой рост", reply_markup=markup)
            context.user_data[NAME_CONST_CURRENT_STATE_DIALOG] = ASK_GENDER
            return ASK_HEIGHT
        context.user_data[Name_BOT_data].height = height
        # Создаем простую клавиатуру для ответа
        markup_key = creat_markup_registration_menu()
        await update.message.reply_text(f"Спасибо! Ваш рост {height} сохранён. ")
        await update.message.reply_text(
        (
            "Выберите ваш пол , пожалуйста \n" 
            "Oтправь /cancel, если стесняешься." 
        ),
        reply_markup=markup_key,
        )
        context.user_data[NAME_CONST_CURRENT_STATE_DIALOG] = ConversationHandler.END
        return ASK_GENDER
    except Exception as ex:
        print(f'Метод ask_height, произошла ошибка с текстом : {ex}')
        return ConversationHandler.END
"""
Запрос веса
"""
async def ask_weight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        text = update.message.text
        if not text.isdigit():
            markup = creat_markup_registration_menu()
            await update.message.reply_text("Bведите пожалуйста число\n Давай попробуем снова, введите свой вес", reply_markup=markup)
            context.user_data[NAME_CONST_CURRENT_STATE_DIALOG] = ASK_HEIGHT
            return ASK_WEIGHT
        weight = float(text)
        if weight < 2 or weight > 635:
            markup = creat_markup_registration_menu()
            await update.message.reply_text("Кажется ваши весы сломаны\n Давай попробуем снова, введите свой вес", reply_markup=markup)
            context.user_data[NAME_CONST_CURRENT_STATE_DIALOG] = ASK_HEIGHT
            return ASK_WEIGHT
        context.user_data[Name_BOT_data].weight = weight
        markup_key = creat_markup_registration_menu()
        await update.message.reply_text(f"Спасибо! Ваш вес {weight} сохранён.")
        await update.message.reply_text(
            (
                "Введите ваш рост , пожалуйста \n" 
                "Oтправь /skip, если стесняешься." 
            ),
            reply_markup=markup_key,
        )
        context.user_data[NAME_CONST_CURRENT_STATE_DIALOG] = ASK_GENDER
        return ASK_HEIGHT
    except Exception as ex:
        print(f'Метод ask_weight, произошла ошибка с текстом : {ex}')
        return ConversationHandler.END

"""
Запрос возраста
"""
async def ask_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        text = update.message.text
        if not text.isdigit():
            markup = creat_markup_registration_menu()
            await update.message.reply_text("Столько не живут, введите пожалуйста число", reply_markup=markup)
            context.user_data[NAME_CONST_CURRENT_STATE_DIALOG] = ASK_WEIGHT
            return ASK_AGE
        age = int(text)
        if age < 0 or age > 100:
            markup = creat_markup_registration_menu()
            await update.message.reply_text("Не брат, столько не живут. Укажите возраст от 1 до 99.", reply_markup=markup)
            context.user_data[NAME_CONST_CURRENT_STATE_DIALOG] = ASK_WEIGHT
            return ASK_AGE
        context.user_data[Name_BOT_data].age = age
        markup_key = creat_markup_registration_menu()
        await update.message.reply_text(f"Спасибо! Ваш возраст {age} сохранён.\n")
        # Следующее сообщение с удалением клавиатуры `ReplyKeyboardRemove`
        await update.message.reply_text(
            (
                "Введите ваш вес , пожалуйста \n" 
                "Oтправь /skip, если стесняешься." 
            ),
            reply_markup=markup_key
        )
        context.user_data[NAME_CONST_CURRENT_STATE_DIALOG] = ASK_HEIGHT
        return ASK_WEIGHT
    except Exception as ex:
        print(f'Метод ask_age, произошла ошибка с текстом : {ex}')
        return ConversationHandler.END

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Регистрация отменена.")
    return ConversationHandler.END
async def register_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(text="Укажите свой возраст")
    # Следующее сообщение с удалением клавиатуры `ReplyKeyboardRemove`
    markup_key = creat_markup_registration_menu()
    await update.message.reply_text(
        'Oтправь /skip, если стесняешься.',
        reply_markup=markup_key,
    )
    context.user_data[NAME_CONST_CURRENT_STATE_DIALOG] = ASK_AGE
    return ASK_AGE

def make_skip_handler(next_step):
    async def skip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        text_end = "Регистрация окончена. \nДля получения информации о себе, введите комманду /my"
        text_next = f"Ладно, перейдем на следующий шаг, укажите пожалуйста {get_state_text(next_step)}"
        markup = creat_markup_registration_menu()

        if get_state_text(next_step) == ASK_CONST_STRING_END:
            if update.message:
                await update.message.reply_text(text_end)
            elif update.callback_query:
                await update.callback_query.message.reply_text(text_end)
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=text_end)
        else:
            if update.message:
                await update.message.reply_text(text_next, reply_markup=markup)
            elif update.callback_query:
                await update.callback_query.message.reply_text(text_next, reply_markup=markup)
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=text_next, reply_markup=markup)
        return next_step
    return skip


#endregion
async def my_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_profile = context.user_data[Name_BOT_data]  = UserProfile.load_foarm(update.effective_user.id)
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
            f"Рост : {user_profile.height or "неизвестно"}\n"
            f"Вес : {user_profile.weight or "неизвестно"}\n"
            f"ИМТ : {user_profile.calc_iwm()} ({user_profile.get_stadia_iwm() or "неизвестно"})\n"
            f"Пол : {user_profile.gender or "неизвестно"}\n"
            f"Возраст : {user_profile.age or "неизвестно"}\n"
            f"почта : {user_profile.email or "неизвестно"}\n"
            f"дата регистрации : {user_profile.register_date or "неизвестно"}\n"
        )
        await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)
    except ValueError as ex:
        print(ex)
    except FileNotFoundError as ex:
        print(ex)
    except RuntimeError as ex:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Не удалось вас определить ({ex})")
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        answer = (
            "Для начала регистрации /reg.\n"
            "Для получения сохраненной информации о себе /my. \n"
        )
        await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)
        
async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Я не знаю, что делает в данной ситуации, попробуй снова")
    await help_command(update=update, context=context)