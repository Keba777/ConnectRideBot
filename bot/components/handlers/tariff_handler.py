from telegram import InlineKeyboardButton, Update
from telegram.ext import CallbackContext
from telegram_bot_pagination import InlineKeyboardPaginator

from data.location_data import locations


async def format_location(location):
    tariff_per_km = 20
    total_tariff = location['distance'] * tariff_per_km

    formatted_text = "🚖  <b>Estimated Fare</b>\n\n"
    formatted_text += f"<b>Start:</b> {location['start']}\n"
    formatted_text += f"<b>Destination:</b> {location['destination']}\n"
    formatted_text += f"<b>Distance:</b> {location['distance']} km\n"
    formatted_text += f"<b>Tariff:</b> {total_tariff} Birr"
    return formatted_text


async def tariff_command(update: Update, context: CallbackContext):
    paginator = InlineKeyboardPaginator(
        len(locations),
        data_pattern='location#{page}'
    )

    formatted_location = await format_location(locations[0])

    await update.message.reply_text(
        text=formatted_location,
        reply_markup=paginator.markup,
        parse_mode='HTML'
    )


async def tariffs_page_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    page = int(query.data.split('#')[1])

    paginator = InlineKeyboardPaginator(
        len(locations),
        current_page=page,
        data_pattern='location#{page}'
    )

    formatted_location = await format_location(locations[page - 1])

    await query.edit_message_text(
        text=formatted_location,
        reply_markup=paginator.markup,
        parse_mode='HTML'
    )
