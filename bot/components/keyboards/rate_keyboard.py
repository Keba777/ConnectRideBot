from telegram import (ReplyKeyboardMarkup, KeyboardButton)


rate_us_keyboard = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="⭐️ Rate Us"),
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)

rate_passenger_keyboard = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="⭐️ Rate Passenger"),
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)
