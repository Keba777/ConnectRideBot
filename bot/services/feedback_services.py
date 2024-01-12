import requests
from dotenv import load_dotenv
import os
load_dotenv()
API_URL = os.getenv('API_URL')


def create_feedback(feedback):
    url = f"{API_URL}/feedbacks"
    payload = {
        "feedback": feedback,
    }
    response = requests.post(url, json=payload)
    return response.json()
