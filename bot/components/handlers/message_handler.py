from telegram import Update
from telegram.ext import ContextTypes


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    start_text = (
        f"🚗 **ConnectRideBot** 🚗\n\n"
        f"Hello {user_name}! Welcome to ConnectRideBot. To get started, type /info to learn about the bot's features."
    ).replace('!', r'\!').replace('.', r'\.').replace('#', r'\.')

    await update.message.reply_text(start_text, parse_mode='MarkdownV2')


async def feedback_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    feedback_text = (
        "📣 **Submit Feedback** 📣\n\n"
        "To submit feedback about ConnectRideBot, type your feedback message directly in the chat. "
        "We appreciate your thoughts and suggestions!"
    ).replace('!', r'\!').replace('.', r'\.').replace('#', r'\.')

    await update.message.reply_text(feedback_text, parse_mode='MarkdownV2')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🤖 **ConnectRideBot Help** 🤖\n\n"
        "Here are some commands you can use:\n\n"
        "/start - Start the bot and choose an option\n"
        "/info - Learn about ConnectRideBot's features\n"
        "/auth - Begin the authentication process\n"
        "/profile - Manage your profile\n"
        "/feedback - Submit feedback about the bot\n"
        "/help - Display this help message"
    ).replace('!', r'\!').replace('.', r'\.').replace('#', r'\.')

    await update.message.reply_text(help_text, parse_mode='MarkdownV2')


async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    info_text = (
        f"👋 **Welcome to ConnectRideBot, {user_name}!** 👋\n\n"
        "🚗 ConnectRideBot is your ridesharing companion with key features:\n\n"
        "🔐 **User Authentication:** Sign up and log in using your Telegram account.\n"
        "🔄 **Profile Management:** Edit your details like name and contact information.\n"
        "🚖 **Ride Booking:** Request rides, get fare estimates, and view ride history.\n"
        "🚦 **Driver Matching:** Receive alerts, know when a driver accepts your request.\n"
        "⭐ **Rating and Reviews:** Rate rides, provide feedback, and view driver ratings.\n"
        "📚 **History and Receipts:** View ride history and get digital receipts.\n\n"
        "Enjoy your rides with ConnectRideBot! 🌟"
    ).replace('!', r'\!').replace('.', r'\.').replace('#', r'\.')

    await update.message.reply_text(info_text, parse_mode='MarkdownV2')


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} cause error {context.error}")
