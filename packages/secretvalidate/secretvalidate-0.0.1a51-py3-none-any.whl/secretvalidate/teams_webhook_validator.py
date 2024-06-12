
import requests

from secretvalidate.env_loader import get_secret_active, get_secret_inactive
from secretvalidate.session_manager import get_session


# Use the shared session
session = get_session()

def validate_teams_webhook(webhook_url, response):
    """Validate Teams webhook URL."""
    payload = {'text': ''}
    headers = {'Content-Type': 'application/json'}

    try:
        response_data = session.post(
            webhook_url, json=payload, headers=headers)
        response_body = response_data.text

        if response_data.status_code == 400:
            if 'Text is required' in response_body:
                if response:
                    return get_secret_active()
                else:
                    return "Teams webhook URL validation successful!"
            else:
                if response:
                    return get_secret_inactive()
                else:
                    return f"Unexpected response body: {response_body}"
        elif response_data.status_code < 200 or response_data.status_code >= 500:
            if response:
                return get_secret_inactive()
            else:
                return f"Unexpected HTTP response status: {response_data.status_code}"
        else:
            if response:
                return get_secret_inactive()
            else:
                return "Unexpected error"
    except requests.exceptions.RequestException as e:
        if response:
            return get_secret_inactive()
        else:
            return str(e)
