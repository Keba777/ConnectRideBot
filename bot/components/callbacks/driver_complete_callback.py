from telegram import Update
from telegram.ext import CallbackContext
from services.user_services import get_user
from services.ride_services import get_rides
from components.keyboards.driver_keyboard import create_complete_paginator
from utils.driver_utils import filter_rides_by_status, format_ride_info, filter_rides_by_driver


async def driver_complete_page_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    page = int(query.data.split('#')[1])
    user_data = await get_user(update.effective_chat.id)
    userId = user_data.get('_id')

    rides = await get_rides(userId)
    ride_requests = filter_rides_by_status(rides, 'accepted')
    accepted_rides = filter_rides_by_driver(
        ride_requests, update.effective_chat.id)

    paginator = create_complete_paginator(
        len(accepted_rides), page, 'page#{page}')

    if accepted_rides:
        accepted_rides = accepted_rides[page-1]

        ride_info = format_ride_info(accepted_rides)

        context.user_data['current_ride_info'] = accepted_rides

        await query.edit_message_text(
            text=ride_info,
            reply_markup=paginator.markup,
            parse_mode='HTML'
        )
