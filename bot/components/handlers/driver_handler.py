from telegram import Update
from telegram.ext import CallbackContext
from services.user_services import get_user
from services.ride_services import get_rides
from components.keyboards.driver_keyboard import create_accept_paginator, create_complete_paginator
from utils.driver_utils import filter_rides_by_status, format_ride_info, filter_rides_by_driver


async def driver_accept_command(update: Update, context: CallbackContext):
    if update.message.text.strip().lower() == "accept ride request":
        user_data = await get_user(update.effective_chat.id)
        userId = user_data.get('_id')

        rides = await get_rides(userId)
        ride_requests = filter_rides_by_status(rides, 'requested')

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


async def driver_complete_command(update: Update, context: CallbackContext):
    if update.message.text.strip().lower() == "view ongoing rides":

        user_data = await get_user(update.effective_chat.id)
        userId = user_data.get('_id')

        rides = await get_rides(userId)

        ride_requests = filter_rides_by_status(rides, 'accepted')
        accepted_rides = filter_rides_by_driver(
            ride_requests, update.effective_chat.id)

        paginator = create_complete_paginator(
            len(ride_requests), 0, 'page#{page}')

        if accepted_rides:
            accepted_rides = accepted_rides[0]
            ride_info = format_ride_info(accepted_rides)

            context.user_data['current_ride_info'] = accepted_rides

            if update.message:
                await update.message.reply_text(
                    text=ride_info,
                    reply_markup=paginator.markup,
                    parse_mode='HTML'
                )
