
















# Мурзин И. - объявление состояний разговора для бота и создание 2-х кнопочных клавиатур
(FIRST_CHOOSE, SECOND_CHOOSE, TYPING1, TYPING2, TYPING2A, TYPING3, TYPING3A, TYPING4, TYPING4A, TYPING5, TYPING5A,
 TYPING6, TYPING6A, TYPING7, TYPING7A, TYPING8, TYPING8A, TYPING9, TYPING9A, OUTPUT1, OUTPUT2, OUTPUT3) = range(22)


reply_keyboard = [
    ["Open service", "Instruction"]
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


reply_keyboard1 = [
    ["See all operations with consumables", "Get some info about consumables"],
    ["Add operation with consumables", "Update operation with consumables", "Delete operation with consumables"],
    ["Return to start", "Finish the session"]
]
markup1 = ReplyKeyboardMarkup(reply_keyboard1, one_time_keyboard=True)


args = []












































































































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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # Пермякова Ю. - реализация функции сохранения даты совершения операции с расходником и добавления новой
# операции с расходниками в базе данных, где отдельно присваивается значение каждому ее признаку
async def handle_add_operation(update, context):
    date_volume = update.message.text
    args.append(date_volume)
    (consume, start_value, unit_measure, name_employee, position_employee,
     num_taken, reason, fin_value, data_val) = args
    if add_operation(
            consume, start_value, unit_measure, name_employee, position_employee,
            num_taken, reason, fin_value, data_val):
        await context.bot.send_message(
            chat_id=update.message.chat.id, text="Operation added successfully, result was received! "
                                                 "What else do you want to do?", reply_markup=markup1
        )
        args.clear()
        return SECOND_CHOOSE
    else:
        await context.bot.send_message(chat_id=update.message.chat.id, text="Error", reply_markup=markup1)
        args.clear()
        return SECOND_CHOOSE


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # Мурзин И. - реализация функции обработчиков сообщений от пользователя телеграмм-ботом:
# начало разговора, доступные состояния, в которые он может перейти, и условия его окончания
def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            FIRST_CHOOSE: [
                MessageHandler(filters.Regex("^Open service$"), working),
                MessageHandler(filters.Regex("^Instruction$"), helping)
            ],
            SECOND_CHOOSE: [
                MessageHandler(filters.Regex("^See all operations with consumables$"), handle_all_operations),
                MessageHandler(filters.Regex("^Get some info about consumables$"), handle_get_volume_consumables),
                MessageHandler(filters.Regex("^Add operation with consumables$"), in_cons_oper_add),
                MessageHandler(filters.Regex("^Update operation with consumables$"), in_id_oper),
                MessageHandler(filters.Regex("^Delete operation with consumables$"), in_id_oper_del),
                MessageHandler(filters.Regex("^Return to start$"), returning)
            ],
            TYPING1: [MessageHandler(filters.TEXT, in_cons_oper)],
            TYPING2: [MessageHandler(filters.TEXT, in_fst_vol_oper)],
            TYPING2A: [MessageHandler(filters.TEXT, in_fst_vol_oper_add)],
            TYPING3: [MessageHandler(filters.TEXT, in_meas_oper)],
            TYPING3A: [MessageHandler(filters.TEXT, in_meas_oper_add)],
            TYPING4: [MessageHandler(filters.TEXT, in_fio_empl_oper)],
            TYPING4A: [MessageHandler(filters.TEXT, in_fio_empl_oper_add)],
            TYPING5: [MessageHandler(filters.TEXT, in_pos_empl_oper)],
            TYPING5A: [MessageHandler(filters.TEXT, in_pos_empl_oper_add)],
            TYPING6: [MessageHandler(filters.TEXT, in_n_taken_oper)],
            TYPING6A: [MessageHandler(filters.TEXT, in_n_taken_oper_add)],
            TYPING7: [MessageHandler(filters.TEXT, in_reas_oper)],
            TYPING7A: [MessageHandler(filters.TEXT, in_reas_oper_add)],
            TYPING8: [MessageHandler(filters.TEXT, in_fin_vol_oper)],
            TYPING8A: [MessageHandler(filters.TEXT, in_fin_vol_oper_add)],
            TYPING9: [MessageHandler(filters.TEXT, in_dt_vol_oper)],
            TYPING9A: [MessageHandler(filters.TEXT, in_dt_vol_oper_add)],
            OUTPUT1: [MessageHandler(filters.TEXT, handle_update_operation)],
            OUTPUT2: [MessageHandler(filters.TEXT, handle_add_operation)],
            OUTPUT3: [MessageHandler(filters.TEXT, handle_delete_operation)]
        },
        fallbacks=[MessageHandler(filters.Regex("^Finish the session$"), finish)]
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
