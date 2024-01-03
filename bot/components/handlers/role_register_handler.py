from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters
from services.ride_services import register_ride
from services.user_services import get_user

CURRENT_LOCATION, DESTINATION = range(2)


async def handle_registration(update: Update, context: CallbackContext) -> int:
    if update.message.text.strip().lower() == "request ride":
        if await get_user(update.effective_chat.id):
            user = await get_user(update.effective_chat.id)
            userId = user['_id']
            context.user_data['user'] = userId
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter your starting location:")
            return CURRENT_LOCATION
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="You're not registered. Use /auth to register.")
            return ConversationHandler.END


async def handle_current_location_input(update: Update, context: CallbackContext) -> int:
    current_location = update.message.text.strip()
    context.user_data['current_location'] = current_location
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Great! Now, please enter your destination:")
    return DESTINATION


async def handle_destination_input(update: Update, context: CallbackContext) -> int:
    destination = update.message.text.strip().lower()
    user = context.user_data['user']
    current_location = context.user_data['current_location']

    response = register_ride(user, current_location, destination)
    if response:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Registration successful!")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Registration failed. Please try again.")

    context.user_data.clear()
    return ConversationHandler.END


register_role_handler = ConversationHandler(
    entry_points=[MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_registration)],
    states={
        CURRENT_LOCATION: [MessageHandler(filters.TEXT, handle_current_location_input)],
        DESTINATION: [MessageHandler(filters.TEXT, handle_destination_input)],
    },
    # Handle unexpected input
    fallbacks=[MessageHandler(filters.TEXT, handle_registration)],

)
