from telegram import (ReplyKeyboardMarkup, KeyboardButton,
                      InlineKeyboardButton, InlineKeyboardMarkup)
from telegram_bot_pagination import InlineKeyboardPaginator


passenger_menu_keyboard = ReplyKeyboardMarkup(
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
                              callback_data='view_completed_rides')],
        [InlineKeyboardButton("View Ongoing Rides",
                              callback_data='view_ongoing_rides')],
        [InlineKeyboardButton("Go Back",
                              callback_data='back_passenger_menu')],
    ]
)


cancel_button = InlineKeyboardButton(
    'Cancel ride', callback_data='cancel#{}')
go_back_button = InlineKeyboardButton(
    'Go back', callback_data='back_history_page')


def create_request_paginator(total_pages, current_page, data_pattern):
    paginator = InlineKeyboardPaginator(
        total_pages,
        current_page=current_page,
        data_pattern=data_pattern
    )
    paginator.add_before(cancel_button)
    paginator.add_after(go_back_button)

    return paginator


def create_complete_paginator(total_pages, current_page, data_pattern):
    paginator = InlineKeyboardPaginator(
        total_pages,
        current_page=current_page,
        data_pattern=data_pattern
    )
    paginator.add_after(go_back_button)

    return paginator
