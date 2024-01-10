from telegram import Update
from telegram.ext import CallbackContext
from services.user_services import get_user
from services.ride_services import get_rides_for_user
from utils.driver_utils import filter_rides_by_status
from utils.passenger_utils import format_ride_info
from components.keyboards.passenger_keyboard import create_complete_paginator


async def passenger_completed_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    user_data = await get_user(update.effective_chat.id)
    userId = user_data.get('_id')

    rides = await get_rides_for_user(userId)
    ride_requests = filter_rides_by_status(rides, 'completed')

    paginator = create_complete_paginator(
        len(ride_requests), 0, 'page#{page}')

    if ride_requests:
        ride_request = ride_requests[0]
        ride_info = format_ride_info(ride_request)

        context.user_data['current_user_ride_info'] = ride_request

        await query.edit_message_text(
            text=ride_info,
            reply_markup=paginator.markup,
            parse_mode='HTML'
        )
    else:
        await query.edit_message_text(
            text="🚗 You have no completed ride requests.",
        )


async def passenger_complete_page_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    page = int(query.data.split('#')[1])
    user_data = await get_user(update.effective_chat.id)
    userId = user_data.get('_id')

    rides = await get_rides_for_user(userId)
    ride_requests = filter_rides_by_status(rides, 'completed')

    paginator = create_complete_paginator(
        len(ride_requests), page, 'page#{page}')

    if ride_requests:
        ride_request = ride_requests[page-1]

        ride_info = format_ride_info(ride_request)

        context.user_data['current_user_ride_info'] = ride_request

        await query.edit_message_text(
            text=ride_info,
            reply_markup=paginator.markup,
            parse_mode='HTML'
        )
