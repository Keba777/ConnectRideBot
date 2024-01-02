from telegram.ext import ApplicationBuilder, CommandHandler
from components.handlers.message_handler import start_handler, help_command, error, profile_command
from components.handlers.registration_handler import registration_handler
from components.handlers.update_handler import update_handler
from components.handlers.auth_handler import auth_command
from config import TOKEN

if __name__ == "__main__":
    print("Starting bot...")
    app = ApplicationBuilder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_handler))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('auth', auth_command))
    app.add_handler(CommandHandler('profile', profile_command))

    app.add_handler(update_handler)
    # app.add_handlers(handlers={
    #     0: [registration_handler],
    #     1: [update_handler]
    # })

    # Error handling
    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=5)
