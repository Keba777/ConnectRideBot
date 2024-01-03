from telegram import Update
from telegram.ext import ContextTypes, CallbackContext
from services.user_services import get_user
from components.keyboards.registration_keyboard import start_keyboard
from components.keyboards.user_keyboard import driver_keyboard, passenger_keyboard


async def auth_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await authentication_handler(update, context)


async def passenger_menu(update: Update, context: CallbackContext, user_data: dict):
    await update.message.reply_text("Welcome to the Passenger Menu!", reply_markup=passenger_keyboard)


async def driver_menu(update: Update, context: CallbackContext, user_data: dict):
    await update.message.reply_text("Welcome to the Driver Menu!", reply_markup=driver_keyboard)


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
        await update.message.reply_text("User does not exist. Please register with button below.", reply_markup=start_keyboard)
