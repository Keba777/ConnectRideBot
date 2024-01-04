from telegram import Update
from telegram.ext import CallbackContext
from components.keyboards.driver_keyboard import accept_request_keyboard
from services.user_services import get_user
from services.ride_services import get_rides


async def driver_callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == 'driver_accept_request':
        user_data = await get_user(update.effective_chat.id)
        userId = user_data.get('_id')

        # Fetch ride requests for the driver
        ride_requests = await get_rides(userId)

        if ride_requests:
            # Display information about the ride requests
            ride_info_text = "\n\n".join([
                f"User: {ride['user']['fullName']}\nPhone: {ride['user']['phone']}\nPickup Location: {ride['currentLocation']}\nDestination: {ride['destination']}"
                for ride in ride_requests
            ])

            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"Here are the ride requests of users:\n\n{ride_info_text}\n\nTo accept a ride, click the button below:",
                reply_markup=accept_request_keyboard
            )
        else:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="You currently don't have any pending ride requests. Keep checking for new requests!"
            )
