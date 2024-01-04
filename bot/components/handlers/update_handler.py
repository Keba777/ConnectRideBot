from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters
from services.user_services import update_user, register_user
from components.keyboards.registration_keyboard import role_keyboard, phone_keyboard

FULL_NAME, PHONE, ROLE = range(3)


async def handle_update(update: Update, context: CallbackContext) -> int:
    if update.message.text.strip().lower() == "editprofile":
        print("Edit Profile command received")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter your full name:")
        return FULL_NAME
    else:
        print("Ending conversation")
        return ConversationHandler.END


async def handle_full_name_input(update: Update, context: CallbackContext) -> int:
    full_name = update.message.text.strip()
    context.user_data['full_name'] = full_name
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Great! Now, please enter your phone number:", reply_markup=phone_keyboard)
    return PHONE


async def handle_phone_input(update: Update, context: CallbackContext) -> int:
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


async def handle_role_input(update: Update, context: CallbackContext) -> int:
    role = update.message.text.strip().lower()
    telegram_id = update.effective_chat.id
    full_name = context.user_data.get('full_name', '')
    phone = context.user_data.get('phone', '')

    data = {'fullName': full_name, 'phone': phone, 'role': role}

    response = await update_user(telegram_id, data)
    if response:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Update successful!")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Updating failed. Please try again.")

    context.user_data.clear()
    return ConversationHandler.END


update_handler = ConversationHandler(
    entry_points=[MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_update)],
    states={
        FULL_NAME: [MessageHandler(filters.TEXT, handle_full_name_input)],
        PHONE: [MessageHandler(filters.TEXT | filters.CONTACT, handle_phone_input)],
        ROLE: [MessageHandler(filters.TEXT, handle_role_input)],
    },
    fallbacks=[MessageHandler(filters.TEXT, handle_update)],
)
