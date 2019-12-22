from __future__ import print_function
import json
import datetime
import dateutil.parser
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def _get_previous_sunday_date():
    utc_now = datetime.datetime.utcnow()
    utc_weekday = utc_now.weekday()
    to_rest = {
        "0": 1,
        "1": 2,
        "2": 3,
        "3": 4,
        "4": 5,
        "5": 6,
        "6": 0,
    }
    sun_utc = datetime.datetime(utc_now.year, utc_now.month, utc_now.day - to_rest[str(utc_weekday)])
    sun = sun_utc.isoformat() + 'Z' # 'Z' indicates UTC time
    return sun


def _get_next_saturday_date():
    utc_now = datetime.datetime.utcnow()
    utc_weekday = utc_now.weekday()
    to_sum = {
        "0": 5,
        "1": 4,
        "2": 3,
        "3": 2,
        "4": 1,
        "5": 0,
        "6": 7,
    }
    sat_utc = datetime.datetime(utc_now.year, utc_now.month, utc_now.day + to_sum[str(utc_weekday)])
    sat = sat_utc.isoformat() + 'Z' # 'Z' indicates UTC time
    return sat


def _get_all_events(service, calendar_id, time_min, time_max, max_results=10):
    events_result = service.events().list(
        calendarId=calendar_id, timeMin=time_min,
        timeMax=time_max,
        maxResults=max_results, singleEvents=True,
        orderBy='startTime'
    ).execute()
    return events_result.get('items', [])


def _print_events(events):
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(f"* {event['summary']} - {start}")


def _get_quantity_of_hours_from_events(events):
    quantity_hours_list = []
    for e in events:
        if e['end'].get('dateTime') is not None and e['start'].get('dateTime') is not None:
            quantity_hours_list.append(dateutil.parser.parse(e['end'].get('dateTime')) - dateutil.parser.parse(e['start'].get('dateTime')))

    quantity_hours = 0
    for d in quantity_hours_list:
        to_sum = d.seconds if d.seconds else 0
        quantity_hours += to_sum
    quantity_hours /= 3600
    return quantity_hours


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Read calendars.json file
    with open('calendars.json', 'r') as calendars:
        calendars_data_json = calendars.read()

    calendars_data = json.loads(calendars_data_json)

    time_min = _get_previous_sunday_date()
    time_max = _get_next_saturday_date()

    time_min_format = time_min.format("YYYY-MM-DD")
    time_max_format = time_max.format("YYYY-MM-DD")
    print(f"Showing events from {time_min_format} to {time_max_format}\n")

    for calendar in calendars_data:
        calendar_name = calendar.get("name")
        print(f"-------Calendar: {calendar_name}-------")
        print(f"Getting the upcoming 10 events of {calendar_name} calendar...")

        calendar_id = calendar.get("id")
        events = _get_all_events(service, calendar_id, time_min, time_max)
        _print_events(events)
        print()

        quantity_hours = _get_quantity_of_hours_from_events(events)
        print(f"Quantity of hours spent in {calendar_name}:", quantity_hours)
        print("\n")
    

if __name__ == '__main__':
    main()