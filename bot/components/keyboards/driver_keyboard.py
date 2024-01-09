from telegram import (ReplyKeyboardMarkup, KeyboardButton,
                      InlineKeyboardButton, InlineKeyboardMarkup)
from telegram_bot_pagination import InlineKeyboardPaginator

driver_keyboard = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Accept ride request"),
            KeyboardButton(text="View ongoing rides"),
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)

driver_menu_keyboard = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Accept ride request",
                              callback_data='accept_ride_request')],
        [InlineKeyboardButton("View Ongoing Rides",
                              callback_data='view_accepted_rides')],
    ]
)


accept_button = InlineKeyboardButton(
    'Accept request', callback_data='accept#{}')
complete_button = InlineKeyboardButton(
    'Complete ride', callback_data='complete#{}')
go_back_button = InlineKeyboardButton(
    'Go back', callback_data='back_driver_menu')


def create_accept_paginator(total_pages, current_page, data_pattern):
    paginator = InlineKeyboardPaginator(
        total_pages,
        current_page=current_page,
        data_pattern=data_pattern
    )
    paginator.add_before(accept_button)
    paginator.add_after(go_back_button)
    return paginator


def create_complete_paginator(total_pages, current_page, data_pattern):
    paginator = InlineKeyboardPaginator(
        total_pages,
        current_page=current_page,
        data_pattern=data_pattern
    )
    paginator.add_before(complete_button)
    paginator.add_after(go_back_button)
    return paginator
