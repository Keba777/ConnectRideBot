from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters
from services.user_services import get_user
from services.rating_services import create_driver_rating

RATING, FEEDBACK = range(2)


async def handle_rating(update: Update, context: CallbackContext) -> int:
    if update.message.text.strip().lower() == "⭐️ rate passenger":
        if await get_user(update.effective_chat.id):
            user = await get_user(update.effective_chat.id)
            userId = user['_id']
            context.user_data['user'] = userId
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Great! Please rate the driver on a scale of 1 to 5, where 1 is the least and 5 is the best.")
            return RATING
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="You're not registered. Use /auth to register.")
            return ConversationHandler.END


async def handle_rating_input(update: Update, context: CallbackContext) -> int:
    rating_str = update.message.text.strip()

    try:
        rating = int(rating_str)
        if 1 <= rating <= 5:
            context.user_data['rating'] = rating
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Awesome! Now, share your feedback about the passenger.")
            return FEEDBACK
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter a rating between 1 and 5.")
            return RATING
    except ValueError:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid input. Please enter a number between 1 and 5.")
        return RATING


async def handle_feedback_input(update: Update, context: CallbackContext) -> int:
    feedback = update.message.text.strip().lower()
    user = context.user_data['user']
    rating = context.user_data['rating']

    response = create_driver_rating(user, rating, feedback)
    if response:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Thank you for submitting feedback! Your opinion matters.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Oops! Something went wrong. Please try again later.")

    context.user_data.clear()
    return ConversationHandler.END


submit_driver_rating = ConversationHandler(
    entry_points=[MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_rating)],
    states={
        RATING: [MessageHandler(filters.TEXT, handle_rating_input)],
        FEEDBACK: [MessageHandler(filters.TEXT, handle_feedback_input)],
    },
    # Handle unexpected input
    fallbacks=[MessageHandler(filters.TEXT, handle_rating)],
)
