from functools import wraps
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, Dispatcher
from bot.actions.instagram.instagram_view import add_instagram_account_view, check_hashtag_view, start, add_state_to_context, add_type_to_context
from bot.actions.instagram.instagram_action import handle_command
from bot.utils import ACTION_KEY


class TelegramBot:
    def __init__(self) -> None:
        self.updater = Updater(token="6833809892:AAE9oa6uOrXGBISxWSxb8_Yxk1OlckZjV9U", use_context=True)
        self.dispatcher:Dispatcher = self.updater.dispatcher


    def config(self):
        self.dispatcher.add_handler(CommandHandler("start",start, run_async=True))
        self.dispatcher.add_handler(MessageHandler(Filters.text(ACTION_KEY.addUser), add_instagram_account_view))
        self.dispatcher.add_handler(MessageHandler(Filters.text(ACTION_KEY.checkhashtag), check_hashtag_view))
        self.dispatcher.add_handler(MessageHandler(Filters.text(ACTION_KEY.women) | Filters.text(ACTION_KEY.men), add_type_to_context))
        self.dispatcher.add_handler(MessageHandler(Filters.text(ACTION_KEY.end), start))

        state_regex = r"ناحیه: (.*)"
        self.dispatcher.add_handler(MessageHandler(Filters.regex(state_regex), add_state_to_context))

        self.dispatcher.add_handler(MessageHandler(Filters.all, handle_command))

        self.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        self.updater.idle()
    