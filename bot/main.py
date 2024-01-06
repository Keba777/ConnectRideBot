import asyncio

from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CallbackQueryHandler, CommandHandler)

from components.callbacks.driver_callback import driver_callback_handler
from components.callbacks.passenger_callback import passenger_callback_handler

from components.handlers.driver_handler import (
    driver_command, driver_page_callback, accept_ride_callback)

from components.handlers.auth_handler import auth_command
from components.handlers.driver_rating_handler import submit_driver_rating
from components.handlers.feedback_handler import feedback_command
from components.handlers.message_handler import (error, help_command,
                                                 info_command, start_command)
from components.handlers.passenger_rating_handler import submit_passenger_rating
from components.handlers.profile_handler import profile_command
from components.handlers.registration_handler import registration_handler
from components.handlers.ride_register_handler import register_role_handler
from components.handlers.update_handler import update_handler
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
    app.add_handler(CommandHandler('rideinfo', driver_command))
    app.add_handler(CommandHandler('start', start_command))

    # Message handlers
    app.add_handlers(handlers={
        0: [submit_driver_rating],
        1: [submit_passenger_rating],
        2: [registration_handler],
        3: [register_role_handler],
        4: [update_handler]
    })

    # Callbacks
    app.add_handlers(handlers={
        0: [CallbackQueryHandler(
            driver_page_callback, pattern='^page#')],
        1: [CallbackQueryHandler(driver_callback_handler)],
        2: [CallbackQueryHandler(passenger_callback_handler)],
        3: [CallbackQueryHandler(accept_ride_callback, pattern='^accept#')]

        # 3: [CallbackQueryHandler(accept_request_callback, pattern=r'^accept#\d+$')],
        # 4: [CallbackQueryHandler(go_back_callback, pattern=r'^back$')]
    })

    # Error handling
    app.add_error_handler(error)

    print("Polling...")
    asyncio.run(app.run_polling(allowed_updates=Update.ALL_TYPES))


if __name__ == "__main__":
    main()
