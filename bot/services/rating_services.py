import requests
from config import API_URL
import logging

logger = logging.getLogger(__name__)


def register_user_rating(user, rating, feedback):
    url = f"{API_URL}/userRatings"
    payload = {
        "user": user,
        "rating": rating,
        "feedback": feedback,
    }
    response = requests.post(url, json=payload)
    return response.json()