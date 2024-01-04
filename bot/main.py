import asyncio

from telegram.ext import (ApplicationBuilder, CallbackQueryHandler,
                          CommandHandler, MessageHandler, filters)

from components.callbacks.driver_callback import driver_callback_handler
from components.callbacks.user_callback import passenger_callback_handler

from components.handlers.auth_handler import auth_command
from components.handlers.feedback_handler import feedback_command
from components.handlers.message_handler import (error, help_command,
                                                 info_command, start_command)
from components.handlers.profile_handler import profile_command
from components.handlers.registration_handler import registration_handler
from components.handlers.ride_register_handler import register_role_handler
from components.handlers.update_handler import update_handler
from components.handlers.user_rating_handler import submit_user_rating

from config import TOKEN


def main():
    print("Starting bot...")
    app = ApplicationBuilder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('auth', auth_command))
    app.add_handler(CommandHandler('feedback', feedback_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('info', info_command))
    app.add_handler(CommandHandler('profile', profile_command))
    app.add_handler(CommandHandler('start', start_command))

    # Messages
    app.add_handler(submit_user_rating)
    app.add_handler(register_role_handler)
    app.add_handlers(handlers={
        0: [registration_handler],
        1: [update_handler],

    })

    # Callbacks
    app.add_handler(CallbackQueryHandler(driver_callback_handler))
    app.add_handler(CallbackQueryHandler(passenger_callback_handler))

    # Error handling
    app.add_error_handler(error)

    print("Polling...")
    asyncio.run(app.run_polling(poll_interval=5))
    # app.run_polling(poll_interval=5)


if __name__ == "__main__":
    main()
