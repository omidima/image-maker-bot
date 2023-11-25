from bot.app_database.database import engine
from bot.twitter_telegram_bot_class import TelegramBot as TwitterBot

from bot.app_database.models import Base
Base.metadata.create_all(bind=engine)


# # states = ["سمنان","میامی","شاهرود","دامغان","مهدیشهر","سرخه"]
# # for i in states:
# #     get_db().add(UserState(id=str(uuid.uuid4()), name=i))
# #     get_db().commit()

twitter = TwitterBot()
twitter.config()