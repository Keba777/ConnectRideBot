from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, CallbackQueryHandler, MessageHandler, filters
from services.ride_services import update_ride


RATING, REVIEW = range(2)


async def passenger_feedback_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    current_ride_info = context.user_data.get('current_user_ride_info', {})
    user_feedback = current_ride_info.get('userFeedback', {})

    if user_feedback is None or (user_feedback.get('rating') is None and user_feedback.get('review') is None):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter your rating on a scale of 1 to 5.")
        return RATING

    await context.bot.send_message(chat_id=update.effective_chat.id, text="You have already provided your feedback.")
    return ConversationHandler.END


async def passenger_rating_input(update: Update, context: CallbackContext):
    try:
        rating = int(update.message.text.strip())
        if 1 <= rating <= 5:
            context.user_data['rating'] = rating
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="Invalid rating. Please enter a numeric rating between 1 and 5.")
            return
    except ValueError:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Invalid input. Please enter a valid numeric rating between 1 and 5.")
        return

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Thanks! Now, please provide your review.")
    return REVIEW


async def passenger_review_input(update: Update, context: CallbackContext):
    current_ride_info = context.user_data.get('current_user_ride_info', {})
    ride_id = current_ride_info.get('_id', '')
    review = update.message.text.strip()

    rating = context.user_data.get('rating', '')
    updated_data = {"userFeedback": {"rating": rating, "review": review}}
    response = await update_ride(ride_id, updated_data)

    if response:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Thank you! Your feedback has been submitted.")


passenger_feedback_callback_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(
        passenger_feedback_callback, pattern='^user_provide_feedback#')],
    states={
        RATING: [MessageHandler(filters.TEXT, passenger_rating_input)],
        REVIEW: [MessageHandler(filters.TEXT, passenger_review_input)]
    },
    fallbacks=[CallbackQueryHandler(
        passenger_feedback_callback, pattern='^user_provide_feedback#')],
)


async def passenger_get_feedback_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    current_ride_info = context.user_data.get('current_user_ride_info', {})
    driver_feedback = current_ride_info.get('driverFeedback', {})

    if driver_feedback is None or (driver_feedback.get('rating') is None and driver_feedback.get('review') is None):

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="No feedback has been provided for this ride yet. Feel free to share your thoughts!",
        )
    else:
        rating = driver_feedback.get('rating')
        review = driver_feedback.get('review')

        feedback_info = f"<b>🚕 Driver Feedback 🚕</b>\n\n" \
                        f"<b>⭐️ Rating:</b> {rating}\n" \
                        f"<b>📝 Review:</b> {review}"

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=feedback_info,
            parse_mode='HTML'
        )
