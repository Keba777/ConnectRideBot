from telegram import Update
from telegram.ext import ContextTypes
from components.keyboards.registration_keyboard import profile_keyboard
from services.user_services import get_user
from components.keyboards.registration_keyboard import start_keyboard


async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_chat.id
    user_data = await get_user(telegram_id)

    if user_data:
        user_info_text = (
            f"Full Name: {user_data.get('fullName', 'N/A')}\n"
            f"Phone: {user_data.get('phone', 'N/A')}\n"
            f"Role: {user_data.get('role', 'N/A')}"
        )

        await update.message.reply_text(
            f"👤Here's your profile information👤\n\n{user_info_text}\n\nTo make changes, click the button below.",
            reply_markup=profile_keyboard
        )
    else:
        await update.message.reply_text(
            "No user data found. Please make sure you are registered or contact support.", reply_markup=start_keyboard
        )
