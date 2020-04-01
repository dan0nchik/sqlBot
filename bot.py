# 1139407419:AAEgdKd38btTS0VIkUVA-Yld968KHc_D4yk
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import sqlite3
from sqlite3 import Error
import os

updater = Updater(token='1139407419:AAEgdKd38btTS0VIkUVA-Yld968KHc_D4yk', use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    user = update.message.from_user
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Привет, <b>{user.first_name}!</b>"
                                                                    f" Напиши /help чтобы узнать, что я могу",
                             parse_mode=telegram.ParseMode.HTML)


def _help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Вот мои команды: "
                                                                    "/sql - я выведу тебе самые популярные запросы"
                                                                    " языка SQL"
                                                                    "  /add_nick - добавлю твой никнейм в нашу базу "
                                                                    "данных")


def sql(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="*[CREATE TABLE]("
                                                                    "https://www.bitdegree.org/learn/sql-commands"
                                                                    "-list#create-table)*",
                             parse_mode=telegram.ParseMode.MARKDOWN_V2)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Извини, я тебя не понял :(")


def create_connection(file):
    connection = None
    try:
        connection = sqlite3.connect(file)
    except Error as e:
        print(e)
    finally:
        if connection:
            cursor = connection.cursor()
            cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users'; ''')
            if cursor.fetchone()[0] == 1:
                print('Table exists')
            else:
                cursor.execute("""CREATE TABLE users (name TEXT, surname TEXT, username TEXT PRIMARY KEY);""")
                connection.commit()
                connection.close()


def addNicks(update, context):
    user = update.message.from_user
    connection = sqlite3.connect(file)
    cursor = connection.cursor()
    print(user.first_name)
    print(user.last_name)
    print(user.username)
    cursor.execute("""INSERT INTO users (name, surname, username) VALUES 
    ('{0}', '{1}', '{2}');""".format(user.first_name, user.last_name, user.username))
    connection.commit()
    connection.close()
    context.bot.send_message(chat_id=update.effective_chat.id, text="Добавлено! Больше эту команду можно не вызывать :)")


if __name__ == '__main__':
    file = os.getcwd() + r"\users.db"
    create_connection(file)
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', _help))
    dispatcher.add_handler(CommandHandler('sql', sql))
    dispatcher.add_handler(CommandHandler('add_nick', addNicks))
    # после этого хэндлера команды в dispatcher добавлять нельзя
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    updater.start_polling()
    updater.idle()
