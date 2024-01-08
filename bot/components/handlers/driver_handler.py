from telegram import Update
from telegram.ext import CallbackContext
from services.user_services import get_user
from services.ride_services import get_rides
from components.keyboards.driver_keyboard import create_accept_paginator
from utils.driver_utils import filter_rides_by_status, format_ride_info


async def driver_command(update: Update, context: CallbackContext, status='requested', paginator=None):
    user_data = await get_user(update.effective_chat.id)
    userId = user_data.get('_id')

    rides = await get_rides(userId)
    ride_requests = filter_rides_by_status(rides, status)

    if paginator is None:
        paginator = create_accept_paginator(
            len(ride_requests), 0, 'page#{page}')

    if ride_requests:
        ride_request = ride_requests[0]
        ride_info = format_ride_info(ride_request)

        context.user_data['current_ride_info'] = ride_request

        if update.message:
            await update.message.reply_text(
                text=ride_info,
                reply_markup=paginator.markup,
                parse_mode='HTML'
            )


async def driver_page_callback(update: Update, context: CallbackContext, status='requested', paginator=None):
    query = update.callback_query
    await query.answer()

    page = int(query.data.split('#')[1])
    user_data = await get_user(update.effective_chat.id)
    userId = user_data.get('_id')

    rides = await get_rides(userId)
    ride_requests = filter_rides_by_status(rides, status)

    if paginator is None:
        paginator = create_accept_paginator(
            len(ride_requests), page, 'page#{page}')

    if ride_requests:
        ride_request = ride_requests[page-1]

        ride_info = format_ride_info(ride_request)

        context.user_data['current_ride_info'] = ride_request

        await query.edit_message_text(
            text=ride_info,
            reply_markup=paginator.markup,
            parse_mode='HTML'
        )
