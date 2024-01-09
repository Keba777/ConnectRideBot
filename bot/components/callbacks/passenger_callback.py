from telegram import Update
from telegram.ext import CallbackContext
from components.keyboards.passenger_keyboard import ride_history_keyboard, passenger_menu_keyboard
from services.ride_services import update_ride
from services.user_services import get_user


async def go_back_to_passenger_menu(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    await context.bot.send_message(
        chat_id=user_id,
        text="Going back to the passenger menu...",
        reply_markup=passenger_menu_keyboard
    )


async def go_back_to_history(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    await context.bot.send_message(
        chat_id=user_id,
        text="Going back to the history page...",
        reply_markup=ride_history_keyboard
    )


async def passenger_cancel_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    current_ride_info = context.user_data.get('current_user_ride_info', '')
    ride_id = current_ride_info.get('_id', '')
    assigned_driver_id = current_ride_info.get(
        'driver', {}).get('telegramId', '')

    telegram_id = update.effective_chat.id
    passenger_data = await get_user(telegram_id)
    passenger_name = passenger_data.get('fullName', 'N/A')

    updated_data = {'status': 'canceled'}
    response = await update_ride(ride_id, updated_data)

    if response:
        await query.edit_message_text(
            text="Ride Canceled!",
            reply_markup=None,
            parse_mode='HTML'
        )

        # Check if there is an assigned driver and send a reminder
        if assigned_driver_id:
            reminder_text = f"{passenger_name} has canceled the ride."
            await context.bot.send_message(
                chat_id=assigned_driver_id,
                text=reminder_text
            )
