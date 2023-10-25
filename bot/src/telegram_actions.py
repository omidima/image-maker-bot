from enum import Enum
import logging
import re
import requests
from telegram import Update
from telegram.ext import Dispatcher, Updater, Filters, MessageHandler
import g4f
from g4f import Provider


from src.context import context_saver


def _get_nonce():
    response = requests.get('https://chatgpt.ai/')
    nonce = re.findall(r'data-nonce="(.*)"', response.text)
    post_id = re.findall(r'data-post-id="(.*)"', response.text)
    data_url = re.findall(r'data-url="(.*)"', response.text)
    bot_id = re.findall(r'data-bot-id="(.*)"', response.text)
    return nonce,bot_id,post_id, data_url


def fetch_response_non_stream(messages):
    chat = ''
    for message in messages:
        chat += '%s: %s\n' % (message['role'], message['content'])
    chat += 'assistant: '

    nonce,bot_id,post_id, data_url = _get_nonce()

    headers = {
        'authority': 'chatgpt.ai',
        'accept': '*/*',
        'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
        'cache-control': 'no-cache',
        'origin': 'https://chatgpt.ai',
        'pragma': 'no-cache',
        'referer': 'https://chatgpt.ai/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        # 'user-agent': agent,
    }
    data = {
        '_wpnonce': nonce,
        'post_id': post_id,
        'url': 'https://chatgpt.ai/',
        'action': 'wpaicg_chat_shortcode_message',
        'message': chat,
        'bot_id': bot_id
    }

    response = requests.post('https://chatgpt.ai/wp-json/mwai-ui/v1/chats/submit', 
                            headers=headers, data=data)

    print(response)
    return  (response.json()['data'])




model = ['gpt-4', 'gpt-3.5-turbo']

def backup(messages):
    # response = g4f.ChatCompletion.create(model='gpt-3.5-turbo', messages=messages, stream=False)
    # print(response)
    return fetch_response_non_stream(messages=messages)

class TelegramActions(Enum):
    START = "start"
    NEW_CHAT = "چت جدید"


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

@context_saver
def start(update: Update, context: Dispatcher):

    reply = backup(context.user_data['messages'])
    m = update.message.reply_text(text=reply, reply_to_message_id=update.message.message_id)
    context.user_data['messages'].append({"role":"assistant","content": reply})

# if __name__ == '__main__':
application = Updater(token="59380367:xey4Dfbe2icMgQa9aVmYTR8QxgMRtlZzR3Jwrlbi",base_url="https://tapi.bale.ai/")
application.bot.delete_webhook()
dispatcher = application.dispatcher

# dispatcher.add_handler(Filters.text())
dispatcher.add_handler(MessageHandler(Filters.all, start))

application.start_polling(allowed_updates=Update.ALL_TYPES)