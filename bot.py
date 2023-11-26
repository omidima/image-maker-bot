from bot.app_database.database import engine
from bot.instagram_telegram_bot_class import TelegramBot as InstagramBot

from bot.app_database.models import Base
Base.metadata.create_all(bind=engine)


telegram = InstagramBot()
telegram.config()
