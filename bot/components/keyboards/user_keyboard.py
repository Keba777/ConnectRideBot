from telegram import (ReplyKeyboardMarkup, KeyboardButton,
                      InlineKeyboardButton, InlineKeyboardMarkup)

passenger_keyboard = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(
            "Request a ride", callback_data='passenger_request_ride')],
        [InlineKeyboardButton("View ride history",
                              callback_data='passenger_view_history')],
    ]
)


register_ride_keyboard = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(
            "Do Registration", callback_data='do_registration')],
        [InlineKeyboardButton("Go Back", callback_data='go_back')],
    ]
)

register_cancel_keyboard = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Go Back", callback_data='go_back_main')],
    ]
)

register_page_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton("Rigister Page")],
    ]
)

driver_keyboard = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Accept ride request",
                              callback_data='driver_accept_request')],
        [InlineKeyboardButton("View ongoing rides",
                              callback_data='driver_view_ongoing')],
    ]
)
