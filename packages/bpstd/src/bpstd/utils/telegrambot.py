from django.conf import settings
from telegram import Bot


# telegram bot token:
API_TOKEN = settings.TELEGRAM_BOT_API_TOKEN


def send_text_msg_to_group(chat_id, msg):
    bot = Bot(API_TOKEN)
    bot.send_message(chat_id=chat_id, text=msg)
