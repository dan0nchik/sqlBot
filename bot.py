from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import telegram
import sqlite3
from sqlite3 import Error
import os
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from googlesearch import search

updater = Updater(token='1139407419:AAEgdKd38btTS0VIkUVA-Yld968KHc_D4yk', use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    user = update.message.from_user
    update.message.reply_text(f"Привет, <b>{user.first_name}!</b>"f" Напиши /help чтобы узнать, что я могу",
                              parse_mode=telegram.ParseMode.HTML)


def _help(update, context):
    update.message.reply_text("Вот мои команды: ""\n/sql - я выведу тебе самые популярные запросы "
                              "языка SQL:\n"
                              "/add_nick - добавлю твой никнейм в нашу базу "
                              "данных\n/get_db - отправлю "
                              "тебе базу данных никнеймов\n"
                              "/create_db - создам для тебя базу\n"
                              "/insert - заполню твою таблицу")


def askSQLCommand(update, context):
    update.message.reply_text("Введи команду SQLLite которая тебе нужна, и я пришлю тебе ссылку с ней.\n"
                              "Например, alter table")
    return 1


def sendLinkToSQLCommand(update, context):
    context.user_data['command'] = update.message.text
    update.message.reply_text("Подожди немного...")
    query = f"sqlite {context.user_data['command']}"
    for j in search(query, tld="co.in", num=10, stop=1, pause=2):
        update.message.reply_text(f"Вроде нашёл\n {j}")
    return ConversationHandler.END


def unknown(update, context):
    update.message.reply_text("Извини, я тебя не понял :(")


def sendBase(update, context):
    update.message.reply_text("Тссс, это секретная информация...")
    context.bot.send_document(chat_id=update.effective_chat.id, document=open(r"{}\users.db".format(os.getcwd()), 'rb'))


def startCreatingDB(update, context):
    update.message.reply_text("Ты всегда можешь отменить создание базы командой /stop. Готов? Пиши ок")
    return 1


def getDBName(update, context):
    update.message.reply_text("Ну что, создадим базу? А как она будет называться?")
    return 2


def column(update, context):
    context.user_data['name'] = update.message.text
    update.message.reply_text(f"А как будет называться колонка? (Она у нас будет одна, больше делать мне лень)")
    return 3


def columnType(update, context):
    replies = [['INTEGER', 'TEXT']]
    context.user_data['colName'] = update.message.text
    update.message.reply_text(f"Неплохо, записал. \n" f"Какой тип будет у колонки (INTEGER или TEXT)?",
                              reply_markup=ReplyKeyboardMarkup(replies, one_time_keyboard=True))
    return 4


def createDBUserData(update, context):
    context.user_data['type'] = update.message.text
    update.message.reply_text("Обрабатываю твою информацию...", reply_markup=ReplyKeyboardRemove())
    user = update.message.from_user
    folder = user.username
    if folder is None:
        folder = user.last_name
        if folder is None:
            folder = user.first_name
    try:
        os.mkdir(os.getcwd() + r"\{}".format(folder))
    except OSError as error:
        print(error)
    path = os.getcwd() + r"\{}".format(folder) + r"\{}.db".format(context.user_data['name'])
    print(path)
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(f"""CREATE TABLE {context.user_data['name']}
                                 ({context.user_data['colName']} {context.user_data['type']});""")
    update.message.reply_text("Создал! Отправляю...")

    context.bot.send_document(chat_id=update.effective_chat.id, document=open(path, 'rb'))
    return ConversationHandler.END


def stop(update, context):
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
                print("Table exists")
            else:
                cursor.execute("""CREATE TABLE users (name TEXT, surname TEXT, username TEXT PRIMARY KEY);""")
                connection.commit()
                connection.close()


def addNicks(update, context):
    user = update.message.from_user
    connection = sqlite3.connect(file)
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO users (name, surname, username) VALUES 
    ('{0}', '{1}', '{2}');""".format(user.first_name, user.last_name, user.username))
    connection.commit()
    connection.close()
    update.message.reply_text("Добавлено! Больше эту команду можно не вызывать :)")


def startFillingTable(update, context):
    update.message.reply_text("Внимание! Если ты еще не сделал таблицу, нажми /stop и создай её командой /create_db."
                              " В другом случае, в какую таблицу ты хочешь заполнить?")
    user = update.message.from_user
    folder = user.username
    if folder is None:
        folder = user.last_name
        if folder is None:
            folder = user.first_name
    path = os.getcwd() + r"\{}".format(folder)
    print(path)
    tables = os.listdir(path)
    print(tables)
    update.message.reply_text(reply_markup=ReplyKeyboardMarkup(tables, one_time_keyboard=True))
    return 1


def getTableNameToFill(update, context):
    context.user_data['table'] = update.message.text
    update.message.reply_text("ОК, а какую колонку мы будем заполнять?")
    user = update.message.from_user
    folder = user.username
    if folder is None:
        folder = user.last_name
        if folder is None:
            folder = user.first_name
    path = os.getcwd() + r"\{}".format(folder) + r"\{}".format(context.user_data['table'])
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute("""PRAGMA table_info({});""".format(context.user_data['table']))
    update.message.reply_text("")
    return 2


def getColumnNameToFill(update, context):
    context.user_data['column'] = update.message.text
    update.message.reply_text("OK, а какой тип будет у колонки?")
    path = os.getcwd() + r"\{}".format() + r"\{}.db".format(context.user_data['name'])
    connection = sqlite3.connect(path)
    cursor = connection.cursor()


if __name__ == '__main__':
    file = os.getcwd() + r"\users.db"
    create_connection(file)
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', _help))
    dispatcher.add_handler(CommandHandler('add_nick', addNicks))
    dispatcher.add_handler(CommandHandler('get_db', sendBase))
    createDatabaseConvHandler = ConversationHandler(
        entry_points=[CommandHandler('create_db', startCreatingDB)],
        states={
            1: [MessageHandler(Filters.text, getDBName)],

            2: [MessageHandler(Filters.text, column, pass_user_data=True)],

            3: [MessageHandler(Filters.text, columnType, pass_user_data=True)],

            4: [MessageHandler(Filters.text, createDBUserData, pass_user_data=True)]
        },

        fallbacks=[CommandHandler('stop', stop)])

    searchSQLCommandsConvHandler = ConversationHandler(
        entry_points=[CommandHandler('sql', askSQLCommand)],
        states={
            1: [MessageHandler(Filters.text, sendLinkToSQLCommand, pass_user_data=True)]
        },
        fallbacks=[CommandHandler('stop', stop)])

    fillTableConvHandler = ConversationHandler(
        entry_points=[CommandHandler('insert', startFillingTable)],
        states={
            1: [MessageHandler(Filters.text, getTableNameToFill, pass_user_data=True)],
            2: [MessageHandler(Filters.text, getColumnNameToFill, pass_user_data=True)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    dispatcher.add_handler(fillTableConvHandler)
    dispatcher.add_handler(searchSQLCommandsConvHandler)
    dispatcher.add_handler(createDatabaseConvHandler)
    # после этого хэндлера команды в dispatcher добавлять нельзя
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    updater.start_polling()
    updater.idle()
