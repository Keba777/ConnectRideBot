from telegram import Update
from telegram.ext import CallbackContext
from services.user_services import get_user
from services.ride_services import get_rides, update_ride
from components.keyboards.driver_keyboard import create_accept_paginator
from utils.driver_utils import filter_rides_by_status, format_ride_info


async def driver_accept_page_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    page = int(query.data.split('#')[1])
    user_data = await get_user(update.effective_chat.id)
    userId = user_data.get('_id')

    rides = await get_rides(userId)
    ride_requests = filter_rides_by_status(rides, 'requested')

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


async def driver_accept_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    current_ride_info = context.user_data.get('current_ride_info', {})
    ride_id = current_ride_info.get('_id', '')

    driver_data = await get_user(update.effective_chat.id)
    driver = driver_data.get('_id')

    updated_data = {'driver': driver, 'status': 'accepted'}
    response = await update_ride(ride_id, updated_data)

    if response:
        await query.edit_message_text(
            text="Ride accepted!",
            reply_markup=None,
            parse_mode='HTML'
        )

        passenger = current_ride_info.get('user', {})
        user_id = passenger.get('telegramId', '')

        await context.bot.send_message(
            chat_id=user_id,
            text=f"<b>Your Ride Request Accepted</b>\n\n"
            f"<b>Driver:</b> {driver_data.get('fullName', 'N/A')}\n"
            f"<b>Phone:</b> {driver_data.get('phone', '')}\n"
            f"<b>Departure:</b> {current_ride_info.get('currentLocation')}\n"
            f"<b>Destination:</b> {current_ride_info.get('destination')}.",
            parse_mode='HTML'
        )
