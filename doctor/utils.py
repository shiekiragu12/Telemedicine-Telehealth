import requests
import base64


def get_authorization():
    # OAuth app credentials
    CLIENT_ID = ''
    CLIENT_SECRET = ''
    ACCOUNT_ID = ''

    # Base64 encode the client ID and client secret
    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    base64_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    # API endpoint
    token_url = "https://zoom.us/oauth/token"

    # Payload for account_credentials grant type
    payload = {
        'grant_type': 'account_credentials',
        'account_id': ACCOUNT_ID,
    }

    # Headers with Authorization and Host
    headers = {
        'Authorization': f'Basic {base64_credentials}',
        'Host': 'zoom.us'
    }

    # Send POST request to exchange credentials for access token
    response = requests.post(token_url, data=payload, headers=headers)

    # Parse the response
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get('access_token')
        return access_token
    else:
        return None


def create_meeting(title, start_time, duration, agenda):
    access_token = get_authorization()
    if not access_token:
        return {'response': {'message': 'no_token'}, 'status': 'failed'}
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    meeting_data = {
        'topic': title,
        'type': 2,  # 1 for Instant Meeting, 2 for scheduled meeting
        'start_time': start_time,
        'duration': duration if duration < 46 else 45,
        'agenda': agenda,
        'settings': {
            "alternative_hosts_email_notification": True,
            "approval_type": 2,
            # "alternative_hosts": "cshamaldas@gmail.com;livesoftwaredeveloper@gmail.com",
            "join_before_host": True,
            "meeting_authentication": False,
        }
    }

    create_meeting_url = 'https://api.zoom.us/v2/users/me/meetings'
    response = requests.post(create_meeting_url, headers=headers, json=meeting_data)
    response_json = response.json()
    if response.status_code == 201:
        meeting_info = response.json()
        join_url = meeting_info.get('join_url')
        start_url = meeting_info.get('start_url')

        return {'join_url': join_url, 'start_url': start_url, 'response': response_json, 'status': 'success'}
    else:
        return {'response': response_json, 'status': 'failed'}
