import asyncio

from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CallbackQueryHandler, CommandHandler, MessageHandler, filters)

from components.callbacks.driver_callback import driver_accept_callback, driver_complete_callback, driver_go_back_callback
from components.callbacks.passenger_requested_callback import passenger_requested_callback, passenger_request_page_callback

from components.handlers.driver_handler import (
    driver_accept_command, driver_complete_command, driver_accept_page_callback, driver_complete_page_callback)


from components.handlers.auth_handler import auth_command
from components.handlers.driver_rating_handler import submit_driver_rating
from components.handlers.feedback_handler import feedback_command
from components.handlers.message_handler import (error, help_command,
                                                 info_command, start_command)
from components.handlers.passenger_rating_handler import submit_passenger_rating
from components.handlers.profile_handler import profile_command
from components.handlers.registration_handler import registration_handler
from components.handlers.ride_register_handler import register_role_handler
from components.handlers.profile_update_handler import update_handler
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

    # Message handlers
    app.add_handlers(handlers={
        0: [MessageHandler(
            filters.TEXT & ~filters.COMMAND, driver_accept_command)],
        1: [MessageHandler(
            filters.TEXT & ~filters.COMMAND, driver_complete_command)],
        # 2: [MessageHandler(
        #     filters.TEXT & ~filters.COMMAND, passenger_requested_command)]
    })
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
            driver_accept_page_callback, pattern='^page#')],
        1: [CallbackQueryHandler(
            driver_complete_page_callback, pattern='^page#')],
        2: [CallbackQueryHandler(driver_accept_callback, pattern='^accept#')],
        3: [CallbackQueryHandler(driver_complete_callback, pattern='^complete#')],
        4: [CallbackQueryHandler(driver_go_back_callback, pattern='back')],
        # Change the pattern for passenger_requested_command and passenger_request_page_callback
        5: [CallbackQueryHandler(passenger_requested_callback, pattern='^view_ongoing_rides')],
        6: [CallbackQueryHandler(passenger_request_page_callback, pattern='^page#')],
    })

    # Error handling
    app.add_error_handler(error)

    print("Polling...")
    asyncio.run(app.run_polling(allowed_updates=Update.ALL_TYPES))


if __name__ == "__main__":
    main()
