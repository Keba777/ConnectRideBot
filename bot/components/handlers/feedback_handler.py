from telegram import Update
from telegram.ext import ContextTypes, CallbackContext
from services.user_services import get_user
from components.keyboards.registration_keyboard import start_keyboard
from components.keyboards.rate_keyboard import rate_us_keyboard, rate_passenger_keyboard


async def feedback_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await rating_handler(update, context)


async def passenger_feedback_menu(update: Update, context: CallbackContext, user_data: dict):
    user = await get_user(update.effective_chat.id)
    userName = user.get('fullName', 'N/A')

    greeting_text = f"👋 Welcome, {userName}!"
    feedback_prompt = "Please share your feedback with us. Your opinion is valuable. 💬"
    rate_us_command = "To rate our service, click the button below."

    full_message = f"{greeting_text}\n\n{feedback_prompt}\n\n{rate_us_command}"

    await update.message.reply_text(
        full_message,
        reply_markup=rate_us_keyboard
    )


async def driver_feedback_menu(update: Update, context: CallbackContext, user_data: dict):
    user = await get_user(update.effective_chat.id)
    userName = user.get('fullName', 'N/A')

    greeting_text = f"👋 Welcome, {userName}!"
    feedback_prompt = "Please share your feedback with us. Your opinion is valuable. 💬"
    rate_us_command = "To rate passenger, click the button below."

    full_message = f"{greeting_text}\n\n{feedback_prompt}\n\n{rate_us_command}"

    await update.message.reply_text(
        full_message,
        reply_markup=rate_passenger_keyboard
    )


async def rating_handler(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_data_response = await get_user(user_id)

    if user_data_response:
        role = user_data_response.get('role', '')
        if role == 'passenger':
            await passenger_feedback_menu(update, context, user_data_response)
        elif role == 'driver':
            await driver_feedback_menu(update, context, user_data_response)
        else:
            await update.message.reply_text(
                "❌ Invalid role. Please sign in with a valid role."
            )
    else:
        await update.message.reply_text(
            "🚫 User does not exist. Please register with the button below.",
            reply_markup=start_keyboard
        )
