from telegram import Update
from telegram.ext import ContextTypes, CallbackContext
from components.keyboards.registration_keyboard import start_keyboard, profile_keyboard
from services.user_services import get_user


async def start_handler(update: Update, context: CallbackContext):
    """Handles the /start command, greets the user, and presents registration and login options."""

    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"Hello {user_name}! Welcome to the bot.\nPlease choose an option:",
        reply_markup=start_keyboard
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sure! Here are some commands you can use:\n\n"
                                    "/start - Start the bot\n"
                                    "/help - Display this help message\n"
                                    "/profile - to show profile of the user")


async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_chat.id
    user_data = await get_user(telegram_id)

    if user_data:
        # Format the user data for display
        user_info_text = (
            f"Full Name: {user_data.get('fullName', 'N/A')}\n"
            f"Phone: {user_data.get('phone', 'N/A')}\n"
            f"Role: {user_data.get('role', 'N/A')}"
        )

        # Send the formatted user data
        await update.message.reply_text(
            f"Your data is as follows:\n\n{user_info_text}\n\nTo edit, click the button below:",
            reply_markup=profile_keyboard
        )
    else:
        await update.message.reply_text(
            "No user data found. Please make sure you are registered or contact support."
        )


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} cause error {context.error}")
