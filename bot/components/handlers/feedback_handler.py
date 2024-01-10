from telegram import Update
from telegram.ext import (CallbackContext, ConversationHandler, MessageHandler,
                          filters, CommandHandler)
from services.feedback_services import create_feedback

FEEDBACK = range(1)


async def feedback_command(update: Update, context: CallbackContext):
    user_first_name = update.message.from_user.first_name
    chat_id = update.effective_chat.id
    welcome_message = f"Welcome, {user_first_name}! 👋 Share your feedback, thoughts, or suggestions about the bot."
    await context.bot.send_message(chat_id, welcome_message)
    return FEEDBACK


async def handle_feedback_input(update: Update, context: CallbackContext):
    feedback = update.message.text.strip()
    response = create_feedback(feedback)

    if response:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Thank you so much for taking the time to share your feedback! 🙏 Your opinion is valuable and helps us improve.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Oops! 😟 Something went wrong on our end. Please try submitting your feedback again later. We apologize for any inconvenience.")

    context.user_data.clear()
    return ConversationHandler.END

feedback_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('feedback', feedback_command)],
    states={
        FEEDBACK: [MessageHandler(filters.TEXT, handle_feedback_input)],
    },
    fallbacks=[CommandHandler('feedback', feedback_command)],
)
