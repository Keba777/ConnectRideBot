from telegram import Update
from telegram.ext import CallbackContext
from bot.components.keyboards.passenger_keyboard import ride_register_keyboard


async def passenger_callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == 'passenger_request_ride':

        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Great! To request a ride, please click the button below and enter your current location and destination.",
            reply_markup=ride_register_keyboard
        )

    elif query.data == 'passenger_view_history':
        # Handle the logic for "View ride history" if needed
        pass
