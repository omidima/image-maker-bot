from telegram import Update
from telegram.ext import Dispatcher
from enum import Enum
from functools import wraps

class ContextKeys(Enum):
    CHALLENGE = "CHALLENGE"
    PHONE_NUMBER = "PHONE_NUMBER"
    CODE = "CODE"
    LOGGING_TO = "LOGGING_TO"
    EITA_CHANNELS = "EITA_CHANNELS"
    SOROUDH_CHANNELS = "SOROUDH_CHANNELS"
    BALE_CHANNELS = "BALE_CHANNELS"
    ACTIVE_COMMAND = "ACTIVE_COMMAND"

def context_saver(func):
    @wraps(func)
    def wrapper(update: Update, context: Dispatcher, *args, **kwargs):
        if context.user_data.get('messages') is None:
            context.user_data['messages'] = []
        
        context.user_data['messages'].append({"role":"user", "content":update.message.text_markdown})
        print(context.user_data['messages'])
        return func(update, context, *args, **kwargs)
    
    return wrapper