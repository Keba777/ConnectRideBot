from telegram import (ReplyKeyboardMarkup, KeyboardButton,
                      InlineKeyboardButton, InlineKeyboardMarkup)


driver_keyboard = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Accept ride request",
                              callback_data='driver_accept_request')],
        [InlineKeyboardButton("View ongoing rides",
                              callback_data='driver_view_ongoing')],
    ]
)

accept_request_keyboard = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Accept ride request"),
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)
