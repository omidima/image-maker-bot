from functools import wraps
from telegram import Update
from telegram.ext import Dispatcher

def use_loading(func):
    @wraps(func)
    def wrapper(update: Update, context: Dispatcher, *args, **kwargs):
      update.message.reply_text(text="در حال پردازش ...")
      result = func(update, context, *args, **kwargs)
      return result

    return wrapper

class ACTION_KEY:
    addUser = "افزودن کاربر"
    checkhashtag = "بررسی هشتگ"
    men = "مردان"
    women = "خواهران"
    end = "پایان"