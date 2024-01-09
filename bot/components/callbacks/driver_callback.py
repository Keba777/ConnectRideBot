from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, CallbackQueryHandler, MessageHandler, filters
from services.ride_services import update_ride
from components.keyboards.driver_keyboard import driver_keyboard

FARE = range(1)


async def driver_complete_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    context.user_data['status'] = 'completed'

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter ride fare!")
    return FARE


async def driver_fare_callback(update: Update, context: CallbackContext):
    current_ride_info = context.user_data.get('current_ride_info', '')
    ride_id = current_ride_info.get('_id', '')

    try:
        fare = float(update.message.text.strip())
    except ValueError:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Invalid fare format. Please enter a valid numeric fare.")
        return

    status = context.user_data.get('status', '')
    updated_data = {'status': status, 'fare': fare}
    response = await update_ride(ride_id, updated_data)

    if response:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Ride Completed!")


driver_complete_callback_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(
        driver_complete_callback, pattern='^complete#')],
    states={
        FARE: [MessageHandler(filters.TEXT, driver_fare_callback)],
    },
    fallbacks=[CallbackQueryHandler(
        driver_complete_callback, pattern='^complete#')],
)


async def driver_go_back_callback(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    await context.bot.send_message(
        chat_id=user_id,
        text="Going back to the driver menu...",
        reply_markup=driver_keyboard
    )
