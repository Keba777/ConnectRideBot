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

ride_register_keyboard = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Request Ride"),
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)
