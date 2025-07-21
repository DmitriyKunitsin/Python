import myLibary as lib
from configs.userData import ASK_AGE
from configs.userData import ASK_WEIGHT
from configs.userData import ASK_HEIGHT
from configs.userData import ASK_GENDER

class FitnessBot:
    def __init__(self, token: str, persistence_path: lib.Optional[str] = None) -> None:
        """
        Инициализация экземпляра бота.

        Args:
            token (str): Токен Telegram-бота для аутентификации.
            persistence_path (lib.Optional[str], optional): Путь к файлу для сохранения состояния бота (постоянство данных). По умолчанию None.
        """
        self.token = token
        self.persistence_path  = persistence_path
        self.application: lib.Optional[lib.Application] = None
    def _setup_event_loop_policy(self) -> None:
        """
        Настройка политики цикла событий asyncio для Windows.

        На Windows по умолчанию используется ProactorEventLoop, 
        который может не работать с некоторыми библиотеками, поэтому здесь переключаем на SelectorEventLoop.
        """
        if lib.sys.platform.startswith("win"):
            lib.asyncio.set_event_loop_policy(lib.asyncio.WindowsSelectorEventLoopPolicy())
    async def setup_bot(self) -> None:
        """
        Асинхронная настройка бота: установка команд и меню.

        Создаёт список команд бота, которые будут отображаться в интерфейсе Telegram,
        а также настраивает меню чата.
        """
        commands = [
            lib.BotCommand("start", "Запустить бота"),
            lib.BotCommand("help", "Помощь"),
            lib.BotCommand("caps", "Капcлок"),
            lib.BotCommand("my", "Информация о себе"),
            lib.BotCommand("reg", "Регистрация")
        ]
        assert self.application is not None
        await self.application.bot.set_my_commands(commands)
        await self.application.bot.set_chat_menu_button(menu_button=lib.MenuButtonCommands())
    def build_keyboard(self, current_list: lib.Optional[lib.List[int]] = None) -> lib.InlineKeyboardMarkup:
        """
        Построение клавиатуры с кнопками для интерфейса Telegram.

        Args:
            current_list (lib.Optional[lib.List[int]], optional): Список идентификаторов или состояний, которые могут влиять на отображение клавиатуры. По умолчанию None.

        Returns:
            lib.InlineKeyboardMarkup: Объект клавиатуры с кнопками для отправки в Telegram.
        """
        buttons = [
            lib.InlineKeyboardButton("Кнопка 1", callback_data="btn1"),
            lib.InlineKeyboardButton("Кнопка 2", callback_data="btn2"),
        ]
        return lib.InlineKeyboardMarkup.from_row(buttons)
    def register_handles(self) -> None:
        """
        Регистрирует обработчики событий для бота.

        Добавляет в приложение различные хендлеры для обработки команд,
        сообщений, inline-запросов и нажатий на кнопки.
        """
        assert self.application is not None
        self.application.add_handler(lib.CommandHandler("start", lib.cmd.start_command))
        # self.application.add_handler(lib.CommandHandler("caps", lib.cmd.caps_command))
        self.application.add_handler(lib.CommandHandler("my",lib.cmd.my_command))
        self.application.add_handler(lib.CommandHandler("help", lib.cmd.help_command))
        
        conv_handler = lib.ConversationHandler(
            entry_points = [
                lib.CommandHandler("reg", lib.cmd.register_command)
            ],
            states={
                ASK_AGE: [lib.MessageHandler(lib.filters.TEXT & ~lib.filters.COMMAND, lib.cmd.ask_age), 
                          lib.CommandHandler('skip', lib.cmd.make_skip_handler(ASK_WEIGHT))],
                ASK_WEIGHT: [lib.MessageHandler(lib.filters.TEXT & ~lib.filters.COMMAND, lib.cmd.ask_weight), 
                             lib.CommandHandler('skip', lib.cmd.make_skip_handler(ASK_HEIGHT))],
                ASK_HEIGHT: [lib.MessageHandler(lib.filters.TEXT & ~lib.filters.COMMAND, lib.cmd.ask_height),
                             lib.CommandHandler('skip', lib.cmd.make_skip_handler(ASK_GENDER))],
                ASK_GENDER: [lib.MessageHandler(lib.filters.Regex('^(Boy|Girl)$'), lib.cmd.ask_gender),
                             lib.CommandHandler('skip', lib.cmd.make_skip_handler(lib.ConversationHandler.END))],
            },
            fallbacks=[lib.CommandHandler('cancel', lib.cmd.cancel)],
        )
        
        self.application.add_handler(conv_handler)
        self.application.add_handler(lib.MessageHandler(lib.filters.TEXT & ~lib.filters.COMMAND, lib.cmd.echo_message))
        self.application.add_handler(lib.MessageHandler(lib.filters.COMMAND, lib.cmd.unknown_message))
        # self.application.add_handler(lib.InlineQueryHandler(lib.cmd.inline_caps))
        # self.application.add_handler(lib.CallbackQueryHandler(lib.cmd.handle_invalid_button, pattern=lib.InvalidCallbackData))
        # self.application.add_handler(lib.CallbackQueryHandler(lib.cmd.list_button))
        
    async def run(self) -> None:
        """
        Запускает бота.

        Настраивает политику цикла событий (особенно для Windows),
        создаёт объект приложения с указанным токеном и опциональной 
        персистентностью, регистрирует обработчики, настраивает команды
        и запускает цикл опроса Telegram.
        """
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

