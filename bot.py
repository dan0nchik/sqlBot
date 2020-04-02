# 1139407419:AAEgdKd38btTS0VIkUVA-Yld968KHc_D4yk
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import telegram
import sqlite3
from sqlite3 import Error
import os
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)

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
                                                                    "данных   /get_db - отправлю "
                                                                    "тебе базу данных никнеймов"
                                                                    " /create_db - создам для тебя базу данных")


def sql(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="*[CREATE TABLE]("
                                                                    "https://www.bitdegree.org/learn/sql-commands"
                                                                    "-list#create-table)*",
                             parse_mode=telegram.ParseMode.MARKDOWN_V2)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Извини, я тебя не понял :(")


def sendBase(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Тссс, это секретная информация...")
    context.bot.send_document(chat_id=update.effective_chat.id, document=open(r"{}\users.db".format(os.getcwd()), 'rb'))


def startCreatingDB(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ты всегда можешь отменить создание базы "
                                                                    "командой /cancel. Готов? Пиши ок")
    return 1


def getDBName(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Ну что, создадим базу? А как она будет называться?")
    return 2


def column(update, context):
    context.user_data['name'] = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"А как будет называться колонка? "
                                                                    "(Она у нас будет одна, больше делать мне лень)")
    return 3


def columnType(update, context):
    replies = [['INTEGER', 'TEXT']]
    context.user_data['colName'] = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Неплохо, записал. "
                                                                    f"Какой тип будет у колонки (INTEGER или TEXT)?",

                             reply_markup=ReplyKeyboardMarkup(replies, one_time_keyboard=True))
    return 4


def createDBUserData(update, context):
    context.user_data['type'] = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text="Обрабатываю твою информацию...",
                             reply_markup=ReplyKeyboardRemove())
    connection = sqlite3.connect(os.getcwd() + r"\{}.db".format(context.user_data['name']))
    cursor = connection.cursor()
    cursor.execute(f"""CREATE TABLE {context.user_data['name']}
                                 ({context.user_data['colName']} {context.user_data['type']});""")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Создал! Отправляю...")

    context.bot.send_document(chat_id=update.effective_chat.id, document=
    open(os.getcwd() + r"\{}.db".format(context.user_data['name']), 'rb'))

    return ConversationHandler.END


def cancel(update, context):
    update.message.reply_text('Пока, жалко базу не сделали :(')
    return ConversationHandler.END


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
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Добавлено! Больше эту команду можно не вызывать :)")


if __name__ == '__main__':
    file = os.getcwd() + r"\users.db"
    create_connection(file)
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', _help))
    dispatcher.add_handler(CommandHandler('sql', sql))
    dispatcher.add_handler(CommandHandler('add_nick', addNicks))
    dispatcher.add_handler(CommandHandler('get_db', sendBase))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('create_db', startCreatingDB)],
        states={
            1: [MessageHandler(Filters.text, getDBName)],

            2: [MessageHandler(Filters.text, column)],

            3: [MessageHandler(Filters.text, columnType)],

            4: [MessageHandler(Filters.text, createDBUserData)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(conv_handler)
    # после этого хэндлера команды в dispatcher добавлять нельзя
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    updater.start_polling()
    updater.idle()
