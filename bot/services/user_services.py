import requests
from config import API_URL
import aiohttp
import logging

logger = logging.getLogger(__name__)


def register_user(telegram_id, full_name, phone, role):
    url = f"{API_URL}/users"
    payload = {
        "telegramId": telegram_id,
        "fullName": full_name,
        "phone": phone,
        "role": role
    }
    response = requests.post(url, json=payload)
    return response.json()


async def get_user(telegram_id: int) -> dict:
    url = f"{API_URL}/users/{telegram_id}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()
    except aiohttp.ClientError as e:
        logger.error(f"Error fetching user: {e}")
        return None


async def update_user(telegram_id, updated_user_data):
    url = f"{API_URL}/users/{telegram_id}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.put(url, json=updated_user_data) as response:
                response.raise_for_status()
                updated_user = await response.json()
                return updated_user
    except aiohttp.ClientError as e:
        logger.error(f"Error updating user: {e}")
        return None
