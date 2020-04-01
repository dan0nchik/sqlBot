# def createDB(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text="Как будет называться база данных?")
#     reply = update.message.from_user
#     connection = sqlite3.connect(os.getcwd() + r"\{}.db".format(reply))
#     cursor = connection.cursor()
#     update.message.reply_text("Создана!")
#     cursor.execute(f'''CREATE TABLE {reply} (id INTEGER);''')
#     context.bot.send_message(chat_id=update.effective_chat.id, text="Сколько в базе будет колонок?")
#     columns = update.message.from_user
#     while columns > 0:
#         context.bot.send_message(chat_id=update.effective_chat.id, text=f"Напиши название {columns} колонки")
#         name = update.message.from_user
#         context.bot.send_message(chat_id=update.effective_chat.id, text=f"Какой у нее будет тип? INTEGER/TEXT ("
#                                                                         f"пиши без пробелов)")
#         DBtype = update.message.from_user
#         cursor.execute(f'''ALTER TABLE {reply} ADD {name} {DBtype};''')
#         context.bot.send_message(chat_id=update.effective_chat.id,
#                                  text=f"Напоминаю: добавлено {name} типа {DBtype}")
#         columns -= 1
#     connection.commit()
#     connection.close()
#     context.bot.send_message(chat_id=update.effective_chat.id, text="Отправляю, смотри не потеряй!")
#     context.bot.send_document(chat_id=update.effective_chat.id,
#                               document=open(r"{0}\{1}".format(os.getcwd(), reply), 'rb'))
#     return ConversationHandler.END