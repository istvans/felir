# -*- coding: utf-8 -*-
"""Object oriented Google Calendar API wrapper to cover our needs."""
import os.path

import click

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


class Calendar:
    """Instantiate to get access to Google Calendar"""

    __CREDENTIALS_FILE = "credentials.json"

    # It stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    _TOKEN_FILE = "token.json"

    # If modifying these scopes, delete the _TOKEN_FILE.
    _SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

    def __init__(self, credentials_file=__CREDENTIALS_FILE, token_file=_TOKEN_FILE):
        creds = None
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, self._SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_file, self._SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_file, 'w') as token:
                token.write(creds.to_json())

        self.__service = build("calendar", "v3", credentials=creds)

    def calendar_id(self, calendar_name):
        """Return the list of ids of the matching calendars."""
        calendars_result = self.__service.calendarList().list().execute()
        calendars = calendars_result.get("items", [])
        matching_calendars = [c for c in calendars if c["summary"] == calendar_name]
        return [cal["id"] for cal in matching_calendars]


@click.command()
@click.option("--name", prompt="The calendar's name", help="The calendar's name.")
def main(name):
    """Show the basic usage of this API."""
    calendar = Calendar()
    print(calendar.calendar_id(name))


if __name__ == '__main__':
    main()

# def main():
#     """Shows basic usage of the Google Calendar API.
#     Prints the start and name of the next 10 events on the user's calendar.
#     """
#     calendar = Calendar()

#     # Call the Calendar API
#     now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

#     print("Getting the upcoming 10 events of '{}'".format(calendar_name))

#     events_result = service.events().list(calendarId=calendar_id, timeMin=now,
#                                           maxResults=10, singleEvents=True,
#                                           orderBy='startTime').execute()
#     events = events_result.get('items', [])

#     if not events:
#         print('No upcoming events found.')
#     for event in events:
#         start = event['start'].get('dateTime', event['start'].get('date'))
#         print(start, event['summary'])


# if __name__ == '__main__':
#     main()
