from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, CallbackQueryHandler, MessageHandler, filters
from services.user_services import get_user
from services.ride_services import get_rides, update_ride
from components.keyboards.driver_keyboard import create_feedback_paginator
from utils.driver_utils import filter_rides_by_status, format_ride_info


async def driver_feedback_page_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    page = int(query.data.split('#')[1])
    user_data = await get_user(update.effective_chat.id)
    userId = user_data.get('_id')

    rides = await get_rides(userId)
    ride_requests = filter_rides_by_status(rides, 'completed')

    paginator = create_feedback_paginator(
        len(ride_requests), page, 'page#{page}')

    if ride_requests:
        ride_request = ride_requests[page-1]

        ride_info = format_ride_info(ride_request)

        context.user_data['current_ride_info'] = ride_request

        await query.edit_message_text(
            text=ride_info,
            reply_markup=paginator.markup,
            parse_mode='HTML'
        )


RATING, REVIEW = range(2)


async def driver_feedback_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    current_ride_info = context.user_data.get('current_ride_info', {})
    driver_feedback = current_ride_info.get('driverFeedback', {})

    if driver_feedback is None or (driver_feedback.get('rating') is None and driver_feedback.get('review') is None):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter your rating on a scale of 1 to 5.")
        return RATING

    await context.bot.send_message(chat_id=update.effective_chat.id, text="You have already provided your feedback.")
    return ConversationHandler.END


async def driver_rating_input(update: Update, context: CallbackContext):
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


async def driver_review_input(update: Update, context: CallbackContext):
    current_ride_info = context.user_data.get('current_ride_info', {})
    ride_id = current_ride_info.get('_id', '')
    review = update.message.text.strip()

    rating = context.user_data.get('rating', '')
    updated_data = {"driverFeedback": {"rating": rating, "review": review}}
    response = await update_ride(ride_id, updated_data)

    if response:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Thank you! Your feedback has been submitted.")


driver_feedback_callback_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(
        driver_feedback_callback, pattern='^driver_provide_feedback#')],
    states={
        RATING: [MessageHandler(filters.TEXT, driver_rating_input)],
        REVIEW: [MessageHandler(filters.TEXT, driver_review_input)]
    },
    fallbacks=[CallbackQueryHandler(
        driver_feedback_callback, pattern='^driver_provide_feedback#')],
)


async def driver_get_feedback_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    current_ride_info = context.user_data.get('current_ride_info', {})
    print(current_ride_info)
    user_feedback = current_ride_info.get('userFeedback', {})
    print(user_feedback)

    if user_feedback is None or (user_feedback.get('rating') is None and user_feedback.get('review') is None):

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="No feedback has been provided for this ride yet. Feel free to share your thoughts!",
        )
    else:
        rating = user_feedback.get('rating')
        review = user_feedback.get('review')

        feedback_info = f"<b>User Feedback</b>\n\n" \
                        f"<b>Rating:</b> {rating}\n" \
                        f"<b>Review:</b> {review}"

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=feedback_info,
            parse_mode='HTML'
        )
