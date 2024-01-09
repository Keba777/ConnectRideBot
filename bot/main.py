import asyncio

from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CallbackQueryHandler, CommandHandler, MessageHandler, filters)

from components.callbacks.driver_callback import driver_accept_callback, driver_complete_callback, driver_go_back_callback
from components.callbacks.passenger_ongoing_callback import passenger_ongoing_callback, passenger_ongoing_page_callback
from components.callbacks.passenger_completed_callback import passenger_completed_callback, passenger_complete_page_callback
from components.callbacks.passenger_callback import go_back_to_history, go_back_to_passenger_menu, passenger_cancel_callback
from components.callbacks.driver_accept_callback import driver_accept_page_callback
from components.callbacks.driver_complete_callback import driver_complete_page_callback

from components.handlers.driver_handler import (
    driver_accept_command, driver_complete_command)


from components.handlers.auth_handler import auth_command
from components.handlers.driver_rating_handler import submit_driver_rating
from components.handlers.feedback_handler import feedback_command
from components.handlers.message_handler import (error, help_command,
                                                 info_command, start_command)
from components.handlers.passenger_rating_handler import submit_passenger_rating
from components.handlers.profile_handler import profile_command
from components.handlers.user_registration_handler import user_registration_handler
from components.handlers.ride_register_handler import register_role_handler
from components.handlers.profile_update_handler import update_handler
from components.handlers.passenger_handler import handle_ride_history
from components.handlers.tariff_handler import tariff_command, tariffs_page_callback
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
    app.add_handler(CommandHandler('tariff', tariff_command))

    # Conversation handlers
    app.add_handlers(handlers={
        0: [user_registration_handler],
        1: [submit_driver_rating],
        2: [submit_passenger_rating],
        3: [register_role_handler],
        4: [update_handler]
    })

    # Message handlers
    app.add_handlers(handlers={
        0: [MessageHandler(
            filters.TEXT & ~filters.COMMAND, driver_accept_command)],
        1: [MessageHandler(
            filters.TEXT & ~filters.COMMAND, driver_complete_command)],
        2: [MessageHandler(
            filters.TEXT & ~filters.COMMAND, handle_ride_history)],
    })

    # Callbacks
    app.add_handlers(handlers={
        0: [CallbackQueryHandler(
            driver_accept_page_callback, pattern='^page#')],
        1: [CallbackQueryHandler(
            driver_complete_page_callback, pattern='^page#')],
        2: [CallbackQueryHandler(driver_accept_callback, pattern='^accept#')],
        3: [CallbackQueryHandler(driver_complete_callback, pattern='^complete#')],
        4: [CallbackQueryHandler(driver_go_back_callback, pattern='back_driver_menu')],
        5: [CallbackQueryHandler(passenger_ongoing_callback, pattern='^view_ongoing_rides')],
        6: [CallbackQueryHandler(passenger_ongoing_page_callback, pattern='^page#')],
        7: [CallbackQueryHandler(passenger_completed_callback, pattern='^view_completed_rides')],
        8: [CallbackQueryHandler(passenger_complete_page_callback, pattern='^page#')],
        9: [CallbackQueryHandler(go_back_to_passenger_menu, pattern='back_passenger_menu')],
        10: [CallbackQueryHandler(go_back_to_history, pattern='back_history_page')],
        11: [CallbackQueryHandler(passenger_cancel_callback, pattern='^cancel#')],
        12: [CallbackQueryHandler(tariffs_page_callback, pattern='^location#')],
    })

    # Error handling
    app.add_error_handler(error)

    print("Polling...")
    asyncio.run(app.run_polling(allowed_updates=Update.ALL_TYPES))


if __name__ == "__main__":
    main()
