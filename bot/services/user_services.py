import requests
from config import API_URL
from logger import logger


def register_user(telegram_id, full_name, phone, role):
    url = f"{API_URL}/users/register"
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
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching user: {e}")
        return None
