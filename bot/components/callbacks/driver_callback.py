from telegram import Update
from telegram.ext import CallbackContext
from services.user_services import get_user
from services.ride_services import update_ride


async def driver_callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == 'driver_accept_request':
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="To accept, use /rideinfo to view user details and click 'Accept request'.",
        )

    elif query.data == 'driver_view_history':
        # Handle the logic for "View ride history" if needed
        pass


async def go_back_callback(update: Update, context: CallbackContext):
    # Add your logic for going back here
    pass


async def accept_ride_callback(update: Update, context: CallbackContext):
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


# async def complete_ride_callback(update: Update, context: CallbackContext):
#     # ... (you can add more callbacks in this file)
