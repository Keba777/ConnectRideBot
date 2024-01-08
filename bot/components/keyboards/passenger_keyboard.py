from telegram import (ReplyKeyboardMarkup, KeyboardButton,
                      InlineKeyboardButton, InlineKeyboardMarkup)


passenger_keyboard = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Request a ride"),
            KeyboardButton(text="View ride history"),
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)


ride_history_keyboard = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("View Completed Rides",
                              callback_data='view_completed')],
        [InlineKeyboardButton("View Ongoing Rides",
                              callback_data='view_ongoing')],
        [InlineKeyboardButton("Go back", callback_data='go_back')],
    ]
)
