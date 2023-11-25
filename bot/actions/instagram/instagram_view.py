from telegram import Update, InputFile, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, Dispatcher
from bot.app_database.database import get_db
from bot.app_database.models import UserState

from bot.utils import ACTION_KEY

def add_instagram_account_view(update:Update, context:Dispatcher):
  # update.message.reply_text("نام حساب‌های کاربری مورد نظر را وارد کنید.")
  context.user_data[0] = ACTION_KEY.addUser
  select_type(update=update,context=context)
  return 0


def add_type_to_context(update:Update, context:Dispatcher):
  context.user_data[1] = update.message.text
  show_state_list(update=update,context=context)
  return 0 


def add_state_to_context(update:Update, context:Dispatcher):
  context.user_data[2] = get_db().query(UserState).filter(UserState.name == update.message.text.replace("ناحیه: ","")).first()
  if (context.user_data[0] == ACTION_KEY.addUser):
    update.message.reply_text("فایل مربوط به حساب‌های کاربری موجود را وارد نمایید.",reply_markup=ReplyKeyboardMarkup([
      [ACTION_KEY.end]
    ]))
  elif (context.user_data[0] == (ACTION_KEY.checkhashtag)):
    update.message.reply_text("هشتگ مورد نظر خود را وارد نمایید.",reply_markup=ReplyKeyboardMarkup([
      [ACTION_KEY.end]
    ]))
  return 0 


def check_hashtag_view(update:Update, context:Dispatcher):
  context.user_data[0] = ACTION_KEY.checkhashtag
  select_type(update=update,context=context)
  return 0


def show_state_list(update:Update, context:Dispatcher):
  states = get_db().query(UserState).all()

  update.message.reply_text("ناحیه مورد نظر خود را انتخاب کنید.", reply_markup=ReplyKeyboardMarkup([
    [f"ناحیه: {state.name}"] for state in states
  ]))
  return 0


def select_type(update:Update, context:Dispatcher):
  update.message.reply_text("گروهان مورد نظر را انتخاب کنید", reply_markup=ReplyKeyboardMarkup([
    [ACTION_KEY.men],
    [ACTION_KEY.women]
  ]))
  return 0


def start(update:Update, context:Dispatcher):
  update.message.reply_text(text="خوش آمدید", reply_markup=ReplyKeyboardMarkup([
      [ACTION_KEY.addUser],
      [ACTION_KEY.checkhashtag],
  ]))
  return 0
