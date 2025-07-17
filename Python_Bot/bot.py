import logging
import asyncio
from my_token import TOKEN
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, InlineQueryHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "Привет! Я твой бот-помощник в мире фитнеса.\n"
        "Я могу быть полезен спортсменам следующим образом:\n"
        "- Отвечаю на вопросы по тренировкам и питанию\n"
        "- Помогаю отслеживать прогресс и ставить цели\n"
        "- Могу напомнить о тренировке или воде\n"
        "- Дам советы по восстановлению и мотивации\n\n"
        "Напиши команду или вопрос, чтобы начать!"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Я не знаю, что делать с этим сообщением")

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Извини, я не понимаю эту команду")

if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(CommandHandler("caps", caps))
    application.add_handler(InlineQueryHandler(inline_caps))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    application.run_polling()
