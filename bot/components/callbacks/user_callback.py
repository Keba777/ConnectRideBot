from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler, MessageHandler, filters, ConversationHandler, CommandHandler


# Components import
from components.keyboards.user_keyboard import passenger_keyboard, register_ride_keyboard, register_cancel_keyboard
from components.handlers.auth_handler import auth_command

# States
MAIN, REGISTER_RIDE = range(2)


async def process_callback_respond_to_register_ride(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    if callback_query:
        print("User clicked Register Ride.")
        await callback_query.message.reply_text(
            "You clicked Register Ride. Use /do_registration to register.", reply_markup=register_ride_keyboard)
    return REGISTER_RIDE


async def process_callback_respond_to_go_back(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    if callback_query:
        await callback_query.message.reply_text(
            "You clicked Go Back. You are now on the main menu.", reply_markup=passenger_keyboard)
    return MAIN


async def process_callback_respond_to_do_registration(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    if callback_query:
        await callback_query.message.reply_text(
            "You clicked Do Registration. Perform the registration here.", reply_markup=register_cancel_keyboard)
    return ConversationHandler.END


async def process_callback_respond_to_go_back_register(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    if callback_query:
        await callback_query.message.reply_text(
            "You clicked Go Back. You are now on the main menu.", reply_markup=passenger_keyboard)
    return MAIN


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text("Sorry, I don't understand that command.")


# Conversation handler
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('auth', auth_command)],
    states={
        MAIN: [
            CallbackQueryHandler(
                process_callback_respond_to_register_ride, pattern='^passenger_request_ride$'),
            CallbackQueryHandler(process_callback_respond_to_go_back, pattern='^go_back$')],
        REGISTER_RIDE: [
            CallbackQueryHandler(
                process_callback_respond_to_do_registration, pattern='^do_registration$'),
            CallbackQueryHandler(process_callback_respond_to_go_back_register, pattern='^go_back_main$')]
    },
    fallbacks=[CallbackQueryHandler(unknown)]
)
