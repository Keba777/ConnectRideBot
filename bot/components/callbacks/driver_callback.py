from telegram import Update
from telegram.ext import CallbackContext
from services.user_services import get_user


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


async def accept_request_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    page = int(query.data.split('#')[1])

    # Get user data based on the page
    user_data = await get_user(update.effective_chat.id)
    userId = user_data.get('_id')

    # Assuming your user data is a dictionary, you can print it to the console
    print(f"Accepting request on page {page}. User data: {user_data}")

    # Add your logic for accepting the request here


async def go_back_callback(update: Update, context: CallbackContext):
    # Add your logic for going back here
    pass
