import logging
import sys
import asyncio
import nest_asyncio
from typing import Optional, Tuple, List, cast
import cmdDir.botCommand as cmd

from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    BotCommand,
    MenuButtonCommands,
    #InlineQueryResultArticle,
    #InputTextMessageContent,
)
from telegram.ext import (
    Application,
    ApplicationBuilder,
    #ContextTypes,
    CommandHandler,
    MessageHandler,
    InlineQueryHandler,
    CallbackQueryHandler,
    filters,
    PicklePersistence,
    InvalidCallbackData,
    ConversationHandler
)


import db.sqliteDb as db
from my_token import TOKEN

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)