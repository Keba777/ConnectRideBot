from telegram import (ReplyKeyboardMarkup, KeyboardButton,
                      InlineKeyboardButton, InlineKeyboardMarkup)

start_keyboard = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Register"),
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)


role_keyboard = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="driver"),
            KeyboardButton(text="passenger")
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)

phone_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton(
            text="Share Phone Number", request_contact=True)
         ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)

profile_keyboard = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="EditProfile"),
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)
