from telegram import Update
from telegram.ext import CallbackContext
from components.keyboards.passenger_keyboard import ride_history_keyboard


async def passenger_go_back_callback(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    await context.bot.send_message(
        chat_id=user_id,
        text="Going back to passenger menu...",
        reply_markup=ride_history_keyboard
    )
