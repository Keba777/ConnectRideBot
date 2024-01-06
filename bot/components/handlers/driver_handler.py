from telegram import InlineKeyboardButton, Update
from telegram.ext import CallbackContext
from telegram_bot_pagination import InlineKeyboardPaginator

from services.user_services import get_user
from services.ride_services import get_rides


async def driver_command(update: Update, context: CallbackContext):
    user_data = await get_user(update.effective_chat.id)
    userId = user_data.get('_id')

    ride_requests = await get_rides(userId)

    paginator = InlineKeyboardPaginator(
        len(ride_requests),
        data_pattern='page#{page}'
    )

    paginator.add_before(
        InlineKeyboardButton(
            'Accept request', callback_data='accept#{}'.format(0)),
    )
    paginator.add_after(InlineKeyboardButton('Go back', callback_data='back'))

    if ride_requests:
        ride_request = ride_requests[0]
        ride_info = format_ride_info(ride_request)

        # Store the ride info in the context
        context.user_data['current_ride_info'] = ride_request

        if update.message:
            await update.message.reply_text(
                text=ride_info,
                reply_markup=paginator.markup,
                parse_mode='HTML'
            )


async def driver_page_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    page = int(query.data.split('#')[1])
    user_data = await get_user(update.effective_chat.id)
    userId = user_data.get('_id')

    ride_requests = await get_rides(userId)

    paginator = InlineKeyboardPaginator(
        len(ride_requests),
        current_page=page,
        data_pattern='page#{page}'
    )

    paginator.add_before(
        InlineKeyboardButton(
            'Accept request', callback_data=f'accept#{page}'
        ),
    )
    paginator.add_after(InlineKeyboardButton('Go back', callback_data='back'))

    if ride_requests:
        ride_request = ride_requests[page-1]

        ride_info = format_ride_info(ride_request)

        # Update the ride info in the context
        context.user_data['current_ride_info'] = ride_request

        await query.edit_message_text(
            text=ride_info,
            reply_markup=paginator.markup,
            parse_mode='HTML'
        )


async def accept_ride_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    # Get the current ride info from the context and print it
    current_ride_info = context.user_data.get('current_ride_info', '')
    print(current_ride_info)


def format_ride_info(ride_request):
    passenger_info = ride_request.get('user', {})
    current_location = ride_request.get('currentLocation', '')
    destination = ride_request.get('destination', '')
    status = ride_request.get('status', '')

    ride_info = (
        "👤 <b>Passenger Details</b>\n"
        f"<b>Name: </b> {passenger_info.get('fullName', '')}\n"
        f"<b>Phone: </b> {passenger_info.get('phone', '')}\n"
        f"<b>Departure: </b> {current_location}\n"
        f"<b>Destination: </b> {destination}\n"
        f"<b>Status: </b> {status}\n"
    )
    return ride_info
