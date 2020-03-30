from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler

updater = Updater(token='1139407419:AAEgdKd38btTS0VIkUVA-Yld968KHc_D4yk', use_context=True)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я - SQL бот!")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()
