import io
from datetime import datetime
import random

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from telegram import Update
from telegram.ext import CallbackContext
from services.user_services import get_user


async def receipt_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    current_ride_info = context.user_data.get('current_user_ride_info', '')
    ride_id = current_ride_info.get('_id', '')
    driver_name = current_ride_info.get('driver', {}).get('fullName', '')
    driver_phone = current_ride_info.get('driver', {}).get('phone', '')

    telegram_id = update.effective_chat.id
    passenger_data = await get_user(telegram_id)
    passenger_name = passenger_data.get('fullName', 'N/A')
    passenger_phone = passenger_data.get('phone', 'N/A')

    current_date_time = datetime.now().strftime('%Y-%m-%d')

    fare = current_ride_info.get('fare', 'N/A')
    departure = current_ride_info.get('currentLocation', 'N/A')
    destination = current_ride_info.get('destination', 'N/A')

    receipt_pdf_bytes = generate_receipt_pdf(
        passenger_name, passenger_phone, departure, destination, fare, current_date_time, driver_name, driver_phone)

    await context.bot.send_document(
        chat_id=telegram_id,
        document=io.BytesIO(receipt_pdf_bytes),
        filename='ride_receipt.pdf',
        caption=f"Thank you for riding with {driver_name}. Here is your receipt."
    )


def generate_receipt_pdf(passenger_name, passenger_phone, departure, destination, fare, ride_date, driver_name, driver_phone):
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=30,
        spaceAfter=24,
        textColor=colors.HexColor('#C05621')
    )
    subheading_style = ParagraphStyle(
        'SubHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        spaceAfter=6,
        alignment=1
    )

    subheading_style_with_border = subheading_style.clone(
        'SubHeadingWithBorder',
        borderBottomColor=colors.blue,
        borderBottomWidth=5,
        spaceAfter=18
    )
    right_aligned_style = ParagraphStyle(
        'RightAligned',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.black,
        alignment=2
    )

    receipt_number = ''.join(
        [str(random.randint(1, 9)) for _ in range(8)])

    content = [
        Paragraph('<b>Connect Ride</b>', title_style),
        Paragraph('<b>Name:</b> {}'.format(passenger_name),
                  subheading_style),
        Paragraph('<b>Phone:</b> {}'.format(passenger_phone),
                  subheading_style_with_border),
        Paragraph('<b>Departure:</b> {}'.format(departure),
                  subheading_style),
        Paragraph('<b>Destination:</b> {}'.format(destination),
                  subheading_style_with_border),

        Paragraph('<b>Driver:</b> {}'.format(driver_name), subheading_style),
        Paragraph('<b>Driver Phone:</b> {}'.format(driver_phone),
                  subheading_style_with_border),
        Paragraph('<b>Total:</b> {}'.format(fare) + ' Birr', subheading_style),
    ]

    top_right_content = [
        Paragraph('<b>Date:</b> {}'.format(ride_date), right_aligned_style),
        Paragraph('<b>Receipt #:</b> {}'.format(receipt_number),
                  right_aligned_style),
    ]

    pdf.build(top_right_content + content)
    buffer.seek(0)
    return buffer.read()
