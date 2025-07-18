import myLibary as lib

class FitnessBot:
    def __init__(self, token: str, persistence_path: lib.Optional[str] = None) -> None:
        self.token = token
        self.persistence_path  = persistence_path
        self.application: lib.Optional[lib.Application] = None
    def _setup_event_loop_policy(self) -> None:
        if lib.sys.platform.startswith("win"):
            lib.asyncio.set_event_loop_policy(lib.asyncio.WindowsSelectorEventLoopPolicy())
    async def setup_bot(self) -> None:
        
        commands = [
            lib.BotCommand("start", "Запустить бота"),
            lib.BotCommand("help", "Помощь"),
            lib.BotCommand("caps", "Каплок"),
            lib.BotCommand("my", "Информация о себе"),
        ]
        assert self.application is not None
        await self.application.bot.set_my_commands(commands)
        await self.application.bot.set_chat_menu_button(menu_button=lib.MenuButtonCommands())
    def build_keyboard(self, current_list: lib.Optional[lib.List[int]] = None) -> lib.InlineKeyboardMarkup:
        # Пример простой клавиатуры с двумя кнопками
        buttons = [
            lib.InlineKeyboardButton("Кнопка 1", callback_data="btn1"),
            lib.InlineKeyboardButton("Кнопка 2", callback_data="btn2"),
        ]
        return lib.InlineKeyboardMarkup.from_row(buttons)
    def register_handles(self) -> None:
        assert self.application is not None
        self.application.add_handler(lib.CommandHandler("start", lib.cmd.start_command))
        self.application.add_handler(lib.MessageHandler(lib.filters.TEXT & ~lib.filters.COMMAND, lib.cmd.echo_message))
        self.application.add_handler(lib.CommandHandler("caps", lib.cmd.caps_command))
        self.application.add_handler(lib.CommandHandler("my",lib.cmd.my_command))
        self.application.add_handler(lib.CommandHandler("help", lib.cmd.help_command))
        self.application.add_handler(lib.InlineQueryHandler(lib.cmd.inline_caps))
        self.application.add_handler(lib.MessageHandler(lib.filters.COMMAND, lib.cmd.unknown_message))
        self.application.add_handler(lib.CallbackQueryHandler(lib.cmd.handle_invalid_button, pattern=lib.InvalidCallbackData))
        self.application.add_handler(lib.CallbackQueryHandler(lib.cmd.list_button))
        
    async def run(self) -> None:
        self._setup_event_loop_policy()
        persistence = (
            lib.PicklePersistence(filepath=self.persistence_path) if self.persistence_path else None
        )
        self.application = (
            lib.ApplicationBuilder()
            .token(self.token)
            .persistence(persistence)
            .arbitrary_callback_data(True)
            .build()
        )
        self.register_handles()
        await self.setup_bot()
        await self.application.run_polling(allowed_updates=lib.Update.ALL_TYPES)

