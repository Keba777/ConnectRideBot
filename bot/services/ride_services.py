import requests
from config import API_URL
import aiohttp
import logging

logger = logging.getLogger(__name__)


# def register_ride(user, current_location, destination, status):
#     url = f"{API_URL}/rides"
#     payload = {
#         "user": user,
#         "currentLocation": current_location,
#         "destination": destination,
#         "status": status
#     }
#     response = requests.post(url, json=payload)
#     return response.json()


async def register_ride(user, current_location, destination, status):
    url = f"{API_URL}/rides"
    payload = {
        "user": user,
        "currentLocation": current_location,
        "destination": destination,
        "status": status
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            return await response.json()
