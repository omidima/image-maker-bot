from pandas import DataFrame
import uuid
from telegram import Update, InputFile
from telegram.ext import Dispatcher
from bot.actions.twitter.twitter_view import show_state_list, select_type
from bot.app_database.database import get_db
from bot.app_database.models import TwitterUserModel, UserState
from bot.twitter_bot import check_user_status
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
    .query(TwitterUserModel)\
    .filter(TwitterUserModel.state_id == context.user_data.get(2).id, TwitterUserModel.isMen == (ACTION_KEY.men == context.user_data.get(1))) \
    .all()
  state = get_db().query(UserState).filter(UserState.id == context.user_data.get(2).id).first()

  twitts = 0
  retwitts = 0
  impration = 0
  comments = 0
  active_user = 0
  for user in users:
    data = check_user_status(username=user.username,hashtag=hashtag)
    if (data.timeline is not None) and (len(data.timeline.twitts) > 0):
      twitts += int(data.timeline.meta.twitts)
      retwitts += int(data.timeline.meta.retwitts)
      impration += sum([int(x.imperation) for x in data.timeline.twitts])
      comments += sum([int(x.comments) for x in data.timeline.twitts])
      active_user+=1

      user_activities.extend([UserStatusDTO(
        username= data.user.username,
        caption=x.text,
        comment_count=x.comments,
        like_count= x.likes,
        hashtag=hashtag,
        retwitt_count=x.retwitte,
        view_count=x.imperation
      ) for x in data.timeline.twitts])

  DataFrame([{
    "نام کاربری": user.username,
    "متن": user.caption,
    "تعداد لایک":user.like_count,
    "تعداد کامنت":user.comment_count,
    "تعداد ویو":user.view_count,
    "تعداد ریتوییت":user.retwitt_count,
  } for user in user_activities]).to_excel("data.xlsx")

  DataFrame([{
    "نام ناحیه": state.name,
    "تعداد توییت": twitts,
    "تعداد ریتوییت": retwitts,
    "تعداد کل ویو‌ها": impration,
    "تعداد کل ریپلای‌ها": comments,
    "گردان":context.user_data.get(1),
    "همه اکانتها": len(users),
    "اکانتهای فعال": active_user,
  }]).to_excel("state.xlsx")

  newData: list[UserStatusDTO] = sorted(user_activities,key=lambda d: int(d.view_count))
  newData = newData if (len(newData)<3) else newData[0:3]

  update.message.reply_document(InputFile(open("data.xlsx","rb").read(), filename="data.xlsx"),caption=f"گزارش آمار افراد بر اساس ناحیه {state.name}")
  update.message.reply_document(InputFile(open("state.xlsx","rb").read(), filename="state.xlsx"),caption=f"گزارش آمار کل ناحیه {state.name}", )
  text = ""
  for i in newData:
    text+=f"""نام کاربری: {i.username}
    متن پست:{i.caption}
    تعداد لایک":{i.like_count}
    تعداد کامنت:{i.comment_count}
    تعداد ویو:{i.view_count}
    تعداد ریتوییت:{i.retwitt_count} \n
------\n
"""
  update.message.reply_text(text=text)

  return 0


def add_user(update:Update, context:Dispatcher):
  db = get_db()

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
    user = db.query(TwitterUserModel).filter(TwitterUserModel.username == username).first()
    if (not user):
      user = TwitterUserModel(id=str(uuid.uuid4()),username=username, user_state=state, isMen=(ACTION_KEY.men == context.user_data.get(1)))
      db.add(user)
      db.commit()
    # user_follow(username)

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