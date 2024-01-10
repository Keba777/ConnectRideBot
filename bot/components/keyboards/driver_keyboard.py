from telegram import (ReplyKeyboardMarkup, KeyboardButton,
                      InlineKeyboardButton)
from telegram_bot_pagination import InlineKeyboardPaginator

driver_keyboard = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Accept ride request"),
            KeyboardButton(text="View ongoing rides"),
        ],
        [
            KeyboardButton(text="Feedback and Ratings"),
        ],
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)


accept_button = InlineKeyboardButton(
    'Accept request', callback_data='accept#{}')
complete_button = InlineKeyboardButton(
    'Complete ride', callback_data='complete#{}')
driver_feedback_button = InlineKeyboardButton(
    'Rate Passenger', callback_data='driver_provide_feedback#{}')
get_feedback_button = InlineKeyboardButton(
    'View Passenger Feedback', callback_data='driver_get_feedback#{}')
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


def create_feedback_paginator(total_pages, current_page, data_pattern):
    paginator = InlineKeyboardPaginator(
        total_pages,
        current_page=current_page,
        data_pattern=data_pattern
    )
    paginator.add_before(driver_feedback_button)
    paginator.add_before(get_feedback_button)
    paginator.add_after(go_back_button)
    return paginator
