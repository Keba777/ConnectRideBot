from telegram import Update
from telegram.ext import CallbackContext
from services.user_services import get_user
from services.ride_services import get_rides


async def driver_accept_command(update: Update, context: CallbackContext):
    if update.message.text.strip().lower() == "accept ride request":
        user_data = await get_user(update.effective_chat.id)
        userId = user_data.get('_id')
