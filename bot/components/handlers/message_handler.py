from telegram import Update
from telegram.ext import ContextTypes, CallbackContext
from components.keyboards.registration_keyboard import start_keyboard


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
                                    "/custom_command - Your custom command")


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} cause error {context.error}")
