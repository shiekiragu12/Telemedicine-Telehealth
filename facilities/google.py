import datetime
from datetime import timedelta

import pytz

from google.oauth2 import service_account

from googleapiclient.discovery import build

from django.conf import settings

service_account_email = "resq247@calendar-events-393013.iam.gserviceaccount.com"
SCOPES = ["https://www.googleapis.com/auth/calendar"]

credentials_path = settings.BASE_DIR / 'config/google_calendar_credentials.json'

credentials = service_account.Credentials.from_service_account_file(credentials_path)
scoped_credentials = credentials.with_scopes(SCOPES)


def build_service():
    service = build("calendar", "v3", credentials=scoped_credentials)
    return service


def create_event():
    service = build_service()

    event = {
        'summary': 'Google I/O 2015',
        'location': '800 Howard St., San Francisco, CA 94103',
        'description': 'A chance to hear more about Google\'s developer products.',
        'start': {
            'dateTime': '2015-05-28T09:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': '2015-05-28T17:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=2'
        ],
        'attendees': [
            {'email': 'dalmasogembo@gmail.com'},
            {'email': 'cshamaldas@gmail.com'},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=30, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    print(events)

    # print(event)
