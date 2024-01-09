import re
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters
from services.user_services import register_user, get_user
from components.keyboards.registration_keyboard import role_keyboard, phone_keyboard

FULL_NAME, PHONE, ROLE = range(3)


async def handle_user_registration(update: Update, context: CallbackContext) -> None:
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
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Great! Now, please share your phone number with the button below:", reply_markup=phone_keyboard)
    return PHONE


async def handle_phone_input(update: Update, context: CallbackContext) -> None:
    phone = None
    if update.message.contact:
        phone = update.message.contact.phone_number

    if phone and is_valid_phone(phone):
        context.user_data['phone'] = phone
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Awesome! Now, please enter your role", reply_markup=role_keyboard)
        return ROLE
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid input. Please share your contact to provide a valid phone number.", reply_markup=phone_keyboard)
        return PHONE


async def handle_role_input(update: Update, context: CallbackContext) -> None:
    role = update.message.text.strip().lower()
    telegram_id = update.effective_chat.id
    full_name = context.user_data['full_name']
    phone = context.user_data['phone']

    if is_valid_role(role):
        response = register_user(telegram_id, full_name, phone, role)
        if response:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Registration successful!")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Registration failed. Please try again.")
        context.user_data.clear()
        return ConversationHandler.END
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid role. Please enter 'passenger' or 'driver' .")
        return ROLE


user_registration_handler = ConversationHandler(
    entry_points=[MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_user_registration)],

    states={
        FULL_NAME: [MessageHandler(filters.TEXT, handle_full_name_input)],
        PHONE: [MessageHandler(filters.CONTACT, handle_phone_input)],
        ROLE: [MessageHandler(filters.TEXT, handle_role_input)],
    },
    # Handle unexpected input
    fallbacks={
        MessageHandler(filters.TEXT, handle_user_registration)
    },

)


def is_valid_phone(phone):
    phone_pattern = re.compile(r'^\+?[1-9]\d{1,14}$')
    return bool(re.match(phone_pattern, phone))


def is_valid_role(role):
    return role in ['passenger', 'driver']
