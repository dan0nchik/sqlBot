# 1139407419:AAEgdKd38btTS0VIkUVA-Yld968KHc_D4yk
from telegram import ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from functools import wraps
import telegram

updater = Updater(token='1139407419:AAEgdKd38btTS0VIkUVA-Yld968KHc_D4yk', use_context=True)
dispatcher = updater.dispatcher


# функция чтобы показать, что бот печатает
def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context, *args, **kwargs)

    return command_func


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я - SQL бот! Напиши /help, "
                                                                    "чтобы узнать, что я могу")


def _help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Вот мои команды: "
                                                                    "/sql - я выведу тебе самые популярные запросы"
                                                                    " языка SQL"
                                                                    "")


def sql(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="*[CREATE TABLE]("
                                                                    "https://www.bitdegree.org/learn/sql-commands-list#create-table)*",
                             parse_mode=telegram.ParseMode.MARKDOWN_V2)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Извини, я тебя не понял :(")


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', _help))
dispatcher.add_handler(CommandHandler('sql', sql))
# после этого хэндлера команды в dispatcher добавлять нельзя
dispatcher.add_handler(MessageHandler(Filters.command, unknown))
updater.start_polling()
updater.idle()
