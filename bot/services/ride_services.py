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


async def get_rides(user: str) -> dict:
    url = f"{API_URL}/rides/{user}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()
    except aiohttp.ClientError as e:
        logger.error(f"Error fetching user: {e}")
        return None


async def update_ride(ride_id, updated_user_data):
    url = f"{API_URL}/rides/{ride_id}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.put(url, json=updated_user_data) as response:
                response.raise_for_status()
                updated_user = await response.json()
                return updated_user
    except aiohttp.ClientError as e:
        logger.error(f"Error updating user: {e}")
        return None
