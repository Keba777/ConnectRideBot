from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters
from services.user_services import register_user, get_user
from components.keyboards.registration_keyboard import role_keyboard, phone_keyboard

FULL_NAME, PHONE, ROLE = range(3)


async def handle_registration(update: Update, context: CallbackContext) -> None:
    if update.message.text.strip().lower() == "register":
        telegram_id = update.effective_chat.id
        if await get_user(telegram_id):
            await context.bot.send_message(chat_id=update.effective_chat.id, text="You're already registered.")
            return ConversationHandler.END

        await context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter your full name:")
        return FULL_NAME


async def handle_full_name_input(update: Update, context: CallbackContext) -> None:
    full_name = update.message.text.strip()
    context.user_data['full_name'] = full_name
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Great! Now, please enter your phone number:", reply_markup=phone_keyboard)
    return PHONE


async def handle_phone_input(update: Update, context: CallbackContext) -> None:
    phone = None
    if update.message.text:
        phone = update.message.text.strip()
    elif update.message.contact:
        phone = update.message.contact.phone_number

    if phone:
        context.user_data['phone'] = phone
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Awesome! Now, please enter your role ", reply_markup=role_keyboard)
        return ROLE
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid input. Please enter a valid phone number or share your contact.")
        return PHONE


async def handle_role_input(update: Update, context: CallbackContext) -> None:
    role = update.message.text.strip().lower()
    telegram_id = update.effective_chat.id
    full_name = context.user_data['full_name']
    phone = context.user_data['phone']

    response = register_user(telegram_id, full_name, phone, role)

    if response:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Registration successful!")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Registration failed. Please try again.")

    context.user_data.clear()
    return ConversationHandler.END

registration_handler = ConversationHandler(
    entry_points=[MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_registration)],

    states={
        FULL_NAME: [MessageHandler(filters.TEXT, handle_full_name_input)],
        PHONE: [MessageHandler(filters.CONTACT, handle_phone_input)],
        ROLE: [MessageHandler(filters.TEXT, handle_role_input)],
    },
    # Handle unexpected input
    fallbacks=[MessageHandler(filters.TEXT, handle_registration)],
)
