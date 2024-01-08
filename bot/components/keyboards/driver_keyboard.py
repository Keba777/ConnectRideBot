from telegram import (ReplyKeyboardMarkup, KeyboardButton,
                      InlineKeyboardButton, InlineKeyboardMarkup)
from telegram_bot_pagination import InlineKeyboardPaginator

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


# Define the inline keyboards
accept_button = InlineKeyboardButton(
    'Accept request', callback_data='accept#{}')
go_back_button = InlineKeyboardButton('Go back', callback_data='back')

# Function to create the paginator


def create_accept_paginator(total_pages, current_page, data_pattern):
    paginator = InlineKeyboardPaginator(
        total_pages,
        current_page=current_page,
        data_pattern=data_pattern
    )
    paginator.add_before(accept_button)
    paginator.add_after(go_back_button)
    return paginator
