
















































































































































# Пермякова Ю. - реализация функции возврата к главному меню телеграмм-бота: выбором между началом работы и инструкцией
async def returning(update, context):
    await context.bot.send_message(
        chat_id=update.message.chat.id,
        text="Hello again! You can open the service or read an instruction about functions of service",
        reply_markup=markup
    )
    return FIRST_CHOOSE


# Пермякова Ю. - реализация функции завершения работы телеграмм-бота (переносит к состоянию до команды /start)
async def finish(update, context):
    await context.bot.send_message(
        chat_id=update.message.chat.id, text="Thank you for using this service. Come back later!",
        reply_markup=ReplyKeyboardRemove()
    )
    args.clear()
    return ConversationHandler.END


# Пермякова Ю. - реализация функции перехода после начала работы к выбору необходимой для пользователя функции
async def working(update, context):
    await context.bot.send_message(
        chat_id=update.message.chat.id, text="Choose the most relevant function, which you want to activate:",
        reply_markup=markup1
    )
    return SECOND_CHOOSE


# Пермякова Ю. - реализация функции вывода для пользователя всех операций с расходниками, имеющихся в базе данных
async def handle_all_operations(update, context):
    message_body = all_operations()
    if message_body:
        await context.bot.send_message(
            chat_id=update.message.chat.id, text=message_body, reply_markup=markup1
        )
        return SECOND_CHOOSE
    else:
        await context.bot.send_message(
            chat_id=update.message.chat.id, text="Error, maybe database is empty", reply_markup=markup1
        )
        return SECOND_CHOOSE


# Пермякова Ю. - реализация функции получения всех операций с расходниками в базе данных по определенным категориям:
# # название расходника, единица его измерения, остаток на дату и сама дата
async def handle_get_volume_consumables(update, context):
    msg = get_volume_consumables()
    if msg:
        await context.bot.send_message(
            chat_id=update.message.chat.id, text=msg, reply_markup=markup1
        )
        return SECOND_CHOOSE
    else:
        await context.bot.send_message(
            chat_id=update.message.chat.id, text="Error, maybe database is empty", reply_markup=markup1
        )
        return SECOND_CHOOSE
