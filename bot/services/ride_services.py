import requests
from config import API_URL
import aiohttp
import logging

logger = logging.getLogger(__name__)


def register_ride(user, current_location, destination):
    url = f"{API_URL}/rides"
    payload = {
        "user": user,
        "currentLocation": current_location,
        "destination": destination,
    }
    response = requests.post(url, json=payload)
    return response.json()



