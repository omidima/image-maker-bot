from pandas import DataFrame
import uuid
from telegram import Update, InputFile
from telegram.ext import Dispatcher
from bot.actions.instagram.instagram_view import show_state_list, select_type
from bot.app_database.database import get_db
from bot.app_database.models import UserModel, UserState
from bot.instagram_bot import check_user_status, user_follow
from bot.utils import ACTION_KEY, use_loading
from bot.utils.classes import UserStatusDTO


def hashtag_status(update:Update, context:Dispatcher):

  # define users gender
  if (context.user_data.get(1) == None):
      select_type(update,context)
      return 0

  # defind state name
  if (context.user_data.get(2) == None):
      show_state_list(update,context)
      return 0

  user_activities : list[UserStatusDTO] = []
  hashtag = update.message.text
  users = get_db() \
    .query(UserModel)\
    .filter(UserModel.state_id == context.user_data.get(2).id, UserModel.isMen == (ACTION_KEY.men == context.user_data.get(1))) \
    .all()
  state = get_db().query(UserState).filter(UserState.id == context.user_data.get(2).id).first()

  for user in users:
    data = check_user_status(username=user.username,hashtag=hashtag)
    if (len(data.status) > 0):
      user_activities.extend(data.status)

  DataFrame([{
    "نام کاربری": temp.username,
    "لینک پست":temp.links,
    "تصویر": temp.media,
    "تعداد لایک":temp.like_count,
    "تعداد کامنت":temp.comment_count,
    "تعداد ویو":temp.view_count,
  } for temp in user_activities]).to_excel("data.xlsx")

  DataFrame([{
    "نام ناحیه": state.name,
    "تعداد فعالیت":len(user_activities),
    "گردان":context.user_data.get(1),
    "همه اکانتها": len(users),
  }]).to_excel("state.xlsx")

  newData = sorted(user_activities,key=lambda d: d.like_count)
  newData = newData if (len(newData)<3) else newData[0:3]

  update.message.reply_document(InputFile(open("data.xlsx","rb").read(), filename="data.xlsx"),caption=f"گزارش آمار افراد بر اساس ناحیه {state.name}")
  update.message.reply_document(InputFile(open("state.xlsx","rb").read(), filename="state.xlsx"),caption=f"گزارش آمار کل ناحیه {state.name}", )
  text = ""
  for i in newData:
    text+=f"""نام کاربری: {i.username},
    لینک پست:{i.links[0]},
    تصویر: {i.media},
    تعداد لایک":{i.like_count},
    تعداد کامنت:{i.comment_count},
    تعداد ویو:{i.view_count} \n
------\n
"""
  update.message.reply_text(text=text)

  return 0


def add_user(update:Update, context:Dispatcher):
  if (context.user_data.get(1) == None):
    select_type(update,context)
    return 0

  if (context.user_data.get(2) == None):
    show_state_list(update,context)
    return 0
    
  state = context.user_data.get(2)
  m = update.message.document
  f = m.get_file().download()
  users = open(f,"r").readlines()

  for temp_username in users:
    username = temp_username.replace("\n","").split("/")[3]
    user = UserModel(id=str(uuid.uuid4()),username=username, user_state=state, isMen=(ACTION_KEY.men == context.user_data.get(1)))
    get_db().add(user)
    get_db().commit()
    user_follow(username)

  update.message.reply_text("موفق")
  context.user_data[0] = None
  context.user_data[1] = None
  context.user_data[2] = None

  return 0


@use_loading
def handle_command(update:Update, context:Dispatcher):
  if context.user_data[0] == ACTION_KEY.addUser:
    add_user(update,context)
  elif context.user_data[0] == ACTION_KEY.checkhashtag:
    hashtag_status(update,context)

  return 0