import time
import requests
from easygoogletranslate import EasyGoogleTranslate

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Dispatcher, Filters, Updater, MessageHandler, CommandHandler


def translator(text):
    translator = EasyGoogleTranslate(
        source_language='auto',
        target_language='en',
        timeout=10
    )
    return translator.translate(text)


def generate(prompt):
    session = requests.Session()
    session.get("https://open.ai")
    en_text = translator(prompt)
    print(en_text)

    session.post("https://open.ai/api/images", json={
        "prompt": en_text,
        "withPromptImprovement": False,
        "useGPU": True
    })

    while True:
        time.sleep(5)
        # try:
        response = session.get("https://open.ai/api/images?page=1&perPage=20")
        print(response.json())
        images = response.json()['images'][0].get("results")
        if (images != None):
            return images[0]['url']
        # except:
        #     pass 


def create_new_image_action(update: Update, context: Dispatcher):
    print("is here")
    if (context.user_data.get("is_active")):
        print("start")
        wait = update.message.reply_text("در حال تولید عکس", reply_to_message_id=update.message.message_id)
        message = update.message.text
        image_url = generate(message)
        context.bot.delete_message(message_id=wait.message_id, chat_id=update.message.chat_id)
        print("end")

        update.message.reply_text(image_url, reply_to_message_id=update.message.message_id)



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
    bot = Updater(token='202825491:K5T18acVPoL6UpLsaMN9GF68KHTlGL1mH216EgZV',
                       base_url="https://tapi.bale.ai/")
    dispatcher = bot.dispatcher

    dispatcher.bot.delete_webhook()
    dispatcher.add_handler(CommandHandler("start",start))
    
    dispatcher.add_handler(MessageHandler(Filters.text("تولید عکس جدید",), create_new_image_view))
    dispatcher.add_handler(MessageHandler(Filters.text("برگشتن به منوی اصلی"), main_menu_view))
    dispatcher.add_handler(MessageHandler(Filters.text("/start"),start))
    dispatcher.add_handler(MessageHandler(Filters.all and ~Filters.command ,create_new_image_action))

    bot.start_polling(allowed_updates=Update.ALL_TYPES)
    bot.idle()


main()

  