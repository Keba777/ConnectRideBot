from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler
from components.handlers.message_handler import start_handler, help_command, error
from components.handlers.registration_handler import registration_handler
from components.handlers.auth_handler import auth_command
from config import TOKEN

if __name__ == "__main__":
    print("Starting bot...")
    app = ApplicationBuilder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_handler))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('auth', auth_command))

    # Registration Process
    app.add_handler(registration_handler)
    # Error handling
    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=3)
