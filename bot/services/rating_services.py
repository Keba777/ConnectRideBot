import requests
from config import API_URL
import logging

logger = logging.getLogger(__name__)


def create_passenger_rating(user, rating, feedback):
    url = f"{API_URL}/passengerRatings"
    payload = {
        "user": user,
        "rating": rating,
        "feedback": feedback,
    }
    response = requests.post(url, json=payload)
    return response.json()


def create_driver_rating(user, rating, feedback):
    url = f"{API_URL}/driverRatings"
    payload = {
        "user": user,
        "rating": rating,
        "feedback": feedback,
    }
    response = requests.post(url, json=payload)
    return response.json()
