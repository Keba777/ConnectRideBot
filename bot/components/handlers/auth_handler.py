from telegram import Update
from telegram.ext import ContextTypes, CallbackContext
from services.user_services import get_user
from components.keyboards.registration_keyboard import start_keyboard


async def auth_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await authentication_handler(update, context)


async def passenger_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
    await update.message.reply_text(
        "Welcome to the Passenger Menu!\n"
        "1. Request a ride\n"
        "2. View ride history\n"
        "3. More options..."
    )


async def driver_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
    await update.message.reply_text(
        "Welcome to the Driver Menu!\n"
        "1. Accept ride request\n"
        "2. View ongoing rides\n"
        "3. More options..."
    )


async def authentication_handler(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_data_response = await get_user(user_id)

    if user_data_response:
        role = user_data_response.get('role', '')
        if role == 'passenger':
            await passenger_menu(update, context, user_data_response)
        elif role == 'driver':
            await driver_menu(update, context, user_data_response)
        else:
            await update.message.reply_text("Invalid role. Please sign in with a valid role.")
    else:
        await update.message.reply_text("User data is incomplete. Please sign in with a valid role.")
