# import re
# from telegram import Update
# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

# from src.telegram_actions import (
#     handle_action_filter,
#     start_view,
#     start_action,
#     get_phone_number_action,
#     check_user_otp_action, end_publish, publish_post_view,
#     add_eita_channel_view
# )
# from src.telegram_menu import SEND_MEDIA, SUBMIT_CHANNEL, LOGIN_TO_ACCOUNT, SUBMIT_EITA_CHANNEL, END


# class TelegramBot:
#     def __init__(
#         self, token: str = "6675106616:AAEvMO5IjiRBXNCwYOE8Rh9nFcMDZ8u3J20"
#     ) -> None:
#         self.updater = Updater(token=token, use_context=True)
#         self.updater.bot.delete_webhook()
#         self.dispatcher = self.updater.dispatcher
#         self.config_bot()

#     def config_bot(self):
#         # start
#         self.dispatcher.add_handler(CommandHandler("start", start_view))
#         self.dispatcher.add_handler(
#             CallbackQueryHandler(
#                 start_action,
#             )
#         )

#         # Phone number
#         # phone_regex = re.compile(r'^09[0-9]{9}$')
#         # phone_filter = Filters.regex(phone_regex)
#         # self.dispatcher.add_handler(MessageHandler(phone_filter, get_phone_number_action))

#         # # Phone number
#         # phone_regex = re.compile(r'^9[0-9]{9}$')
#         # phone_filter = Filters.regex(phone_regex)
#         # self.dispatcher.add_handler(MessageHandler(phone_filter, get_phone_number_action))

#         # # User otp
#         # code_regex = re.compile(r'^[0-9]{5}$')
#         # phone_filter = Filters.regex(code_regex)
#         # self.dispatcher.add_handler(MessageHandler(phone_filter, check_user_otp_action))

#         # Submit channel action
#         # phone_filter = Filters.text(SUBMIT_CHANNEL)
#         # self.dispatcher.add_handler(MessageHandler(phone_filter, check_user_otp_action))

#         # # Login action
#         # phone_filter = Filters.text(LOGIN_TO_ACCOUNT)
#         # self.dispatcher.add_handler(MessageHandler(phone_filter, start_view))

#         # End publish command
#         # end_filter = Filters.text(END)
#         # self.dispatcher.add_handler(MessageHandler(end_filter, end_publish))

#         # # View publish
#         # publish_action = re.compile(SEND_MEDIA)
#         # publish_filter = Filters.regex(publish_action)
#         # self.dispatcher.add_handler(MessageHandler(publish_filter, publish_post_view))

#         # # Submit eita channel
#         # submit_eita_filter = Filters.text(SUBMIT_EITA_CHANNEL)
#         # self.dispatcher.add_handler(MessageHandler(submit_eita_filter, add_eita_channel_view))

#         # Action publish
#         self.dispatcher.add_handler(MessageHandler(Filters.all, handle_action_filter))


#     def get_bot_chats(self):
#         chats = []
#         for item in self.dispatcher.bot.get_updates():
#             chats.append(item.effective_chat.id)

#         return chats

#     def send_message_to_channels(self, channels: list[int], message):
#         for id in channels:
#             self.dispatcher.bot.send_message(chat_id=id, text=message)

#     def start(self):
#         self.updater.start_polling(allowed_updates=Update.ALL_TYPES)
