import requests
from config import API_URL


def create_feedback(feedback):
    url = f"{API_URL}/feedbacks"
    payload = {
        "feedback": feedback,
    }
    response = requests.post(url, json=payload)
    return response.json()
