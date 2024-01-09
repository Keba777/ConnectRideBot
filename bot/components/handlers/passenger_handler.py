from telegram import Update
from telegram.ext import CallbackContext
from components.keyboards.passenger_keyboard import ride_history_keyboard


async def handle_ride_history(update: Update, context: CallbackContext) -> int:
    if update.message.text.strip().lower() == "view ride history":
        message_text = "Here's your ride history. You can view both completed and ongoing rides. Choose an option below:"
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=message_text, reply_markup=ride_history_keyboard
        )
