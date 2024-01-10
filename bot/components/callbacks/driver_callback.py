from telegram import Update
from telegram.ext import CallbackContext
from components.keyboards.driver_keyboard import driver_keyboard


async def driver_go_back_callback(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    await context.bot.send_message(
        chat_id=user_id,
        text="Going back to the driver menu...",
        reply_markup=driver_keyboard
    )
