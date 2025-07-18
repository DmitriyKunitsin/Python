import logging
from my_token import TOKEN
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, InlineQueryHandler, CallbackQueryHandler,InvalidCallbackData,PicklePersistence
from typing import cast

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

    # message = (
    #     "Привет! Я твой бот-помощник в мире фитнеса.\n"
    #     "Я могу быть полезен спортсменам следующим образом:\n"
    #     "- Отвечаю на вопросы по тренировкам и питанию\n"
    #     "- Помогаю отслеживать прогресс и ставить цели\n"
    #     "- Могу напомнить о тренировке или воде\n"
    #     "- Дам советы по восстановлению и мотивации\n\n"
    #     "Напиши команду или вопрос, чтобы начать!"
    # )
    #await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        keyboard = build_keyboard()
        await update.message.reply_text("Выберите действие", reply_markup=keyboard)
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Неудалось обработать комманду")
    

async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Я не знаю, что делать с этим сообщением")

async def caps_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from uuid import uuid4
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(InlineQueryResultArticle(id=uuid4(), title="Caps", input_message_content=InputTextMessageContent(message_text=query.upper())))
    await context.bot.answer_inline_query(update.inline_query.id, results)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer =    ( 
        "Для начала введите команду  /start. \n"
        "Для ответа капсом /caps. \n" 
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)

# def build_keyboard(current_list: list[int]) -> InlineKeyboardMarkup:
#     """Helper function to build the next inline keyboard."""
#     return InlineKeyboardMarkup.from_column(
#         [InlineKeyboardButton(str(i), callback_data=(i, current_list)) for i in range(1, 6)]
#     )
# Функция, которая создаёт клавиатуру с кнопками
def build_keyboard():
    buttons = [
        InlineKeyboardButton("Кнопка 1", callback_data="btn1"),
        InlineKeyboardButton("Кнопка 2", callback_data="btn2"),
    ]
    # Возвращаем разметку с кнопками в один ряд
    return InlineKeyboardMarkup.from_row(buttons)

async def handle_invalid_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Informs the user that the button is no longer available."""
    await update.callback_query.answer()
    await update.effective_message.edit_text(
        "Sorry, I could not process this button click 😕 Please send /start to get a new keyboard."
    )
async def list_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    # Get the data from the callback_data.
    # If you're using a type checker like MyPy, you'll have to use typing.cast
    # to make the checker get the expected type of the callback_data
    number, number_list = cast("tuple[int, list[int]]", query.data)
    # append the number to the list
    number_list.append(number)

    await query.edit_message_text(
        text=f"So far you've selected {number_list}. Choose the next item:",
        reply_markup=build_keyboard(number_list),
    )

    # we can delete the data stored for the query, because we've replaced the buttons
    context.drop_callback_data(query)

async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Извини, я не понимаю эту команду")

if __name__ == "__main__":
    persistence = PicklePersistence(filepath="arbitrarycallbackdatabot")
    application = (
        ApplicationBuilder()
        .token(TOKEN)
        .persistence(persistence)
        .arbitrary_callback_data(True)
        .build()    
    )
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))
    application.add_handler(CommandHandler("caps", caps_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(InlineQueryHandler(inline_caps))
    application.add_handler(MessageHandler(filters.COMMAND, unknown_message))
    application.add_handler(
        CallbackQueryHandler(handle_invalid_button, pattern=InvalidCallbackData)
    )
    application.add_handler(CallbackQueryHandler(list_button))
    application.run_polling(allowed_updates=Update.ALL_TYPES)
