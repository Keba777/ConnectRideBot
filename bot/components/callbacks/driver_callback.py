from telegram import Update
from telegram.ext import CallbackContext
from services.user_services import get_user
from services.ride_services import update_ride


async def driver_accept_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    current_ride_info = context.user_data.get('current_ride_info', '')
    ride_id = current_ride_info.get('_id', '')

    user_data = await get_user(update.effective_chat.id)
    driver = user_data.get('_id')

    updated_data = {'driver': driver, 'status': 'accepted'}
    response = await update_ride(ride_id, updated_data)

    print(response)
    if response:
        await query.edit_message_text(
            text="Ride accepted!",
            reply_markup=None,
            parse_mode='HTML'
        )


async def driver_complete_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    current_ride_info = context.user_data.get('current_ride_info', '')
    ride_id = current_ride_info.get('_id', '')

    updated_data = {'status': 'completed'}
    response = await update_ride(ride_id, updated_data)

    print(response)
    if response:
        await query.edit_message_text(
            text="Ride Completed!",
            reply_markup=None,
            parse_mode='HTML'
        )
