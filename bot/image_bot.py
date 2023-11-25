import os
import random
import time
import uuid
import requests
from easygoogletranslate import EasyGoogleTranslate
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, InputFile
from telegram.ext import Dispatcher, Filters, Updater, MessageHandler, CommandHandler

load_dotenv()

MEDIA_DIR = os.getenv("MEDIA_DIR")


def translator(text):
    translator = EasyGoogleTranslate(
        source_language='auto',
        target_language='en',
        timeout=10
    )
    return translator.translate(text)


def save_image(url):
    if (not os.path.exists(MEDIA_DIR)):
        os.mkdir(MEDIA_DIR)

    response = requests.get(url)
    if (response.status_code == 200):
        name = uuid.uuid4()
        file = open(f"{MEDIA_DIR}/{str(name)}.png","wb")
        file.write(response.content)
        file.close()

        return response.content
    else:
        raise f"Cant download image file: {response.status_code} \n {response.content}"


def generate(prompt):
    session = requests.Session()
    session.get("https://open.ai")
    en_text = translator(prompt)

    session.post("https://open.ai/api/images", json={
        "prompt": en_text,
        "withPromptImprovement": False,
        "useGPU": True
    })

    while True:
        time.sleep(5)
        try:
            response = session.get("https://open.ai/api/images?page=1&perPage=20")
            images = response.json()['images'][0].get("results")
            if (images != None):
                return images[0]['url']
        except:
            return False


def create_new_image_action(update: Update, context: Dispatcher):
    if (context.user_data.get("is_active")):
        wait = update.message.reply_text("در حال تولید عکس", reply_to_message_id=update.message.message_id)
        message = update.message.text
        image_url = generate(message)

        if (image_url):
            file = save_image(image_url)
            update.message.reply_photo(InputFile(file), reply_to_message_id=update.message.message_id)
        else:
            update.message.reply_text("ساختن تصویر ناموفق بود. لطفا تصویر خود را با توضیحات بیشتری توصیف کنید.", reply_to_message_id=update.message.message_id)

        context.bot.delete_message(message_id=wait.message_id, chat_id=update.message.chat_id)


def create_new_image_view(update: Update, context: Dispatcher):
    update.message.reply_text(
        "برای تولید تصویر، ویژگی‌های و خصوصیات عکس خود را توصیف کنید. \n برای مثال: تصویری از یک گل محمدی که یک پروانه بر روی آن نشسته و عکس به صورت پرتره گرفته شده است.",
        reply_markup=ReplyKeyboardMarkup([["برگشتن به منوی اصلی"]])
    )

    context.user_data['is_active'] = True
    return 0


def main_menu_view(update: Update, context: Dispatcher):
    update.message.reply_text(
        "به منوی اصلی بازگشتید",
        reply_markup=ReplyKeyboardMarkup([["تولید عکس جدید"]])
    )

    context.user_data['is_active'] = False
    return 0


def start(update: Update, context: Dispatcher):
    update.message.reply_text(
        "به ربات عکس‌ساز خوش آمدید برای تولید تصویر با هوش‌مصنوعی یک گزینه را انتخاب کنید.",
        reply_markup=ReplyKeyboardMarkup([["تولید عکس جدید"]])
        )
    return 0


def main() : 
    bot = Updater(token="6847148290:AAGTXQivnO8IDr3eNGUqQsAm0A4qN0mjJUM")
    # bot = Updater(token='202825491:K5T18acVPoL6UpLsaMN9GF68KHTlGL1mH216EgZV',
    #                    base_url="https://tapi.bale.ai/")
    dispatcher = bot.dispatcher

    dispatcher.bot.delete_webhook()
    dispatcher.add_handler(CommandHandler("start",start, run_async=True))
    
    dispatcher.add_handler(MessageHandler(Filters.text("تولید عکس جدید",), create_new_image_view, run_async=True))
    dispatcher.add_handler(MessageHandler(Filters.text("برگشتن به منوی اصلی"), main_menu_view, run_async= True))
    dispatcher.add_handler(MessageHandler(Filters.text("/start"),start, run_async= True))
    dispatcher.add_handler(MessageHandler(Filters.all and ~Filters.command ,create_new_image_action, run_async= True))

    bot.start_polling(allowed_updates=Update.ALL_TYPES)
    bot.idle()


main()

  