from datetime import datetime, timedelta
from mail.getGmailService import get_google_service
from langchain_core.tools import tool
from googleapiclient.discovery import build


@tool
def create_calendar_event_tool(summary: str,
    start_time: str, 
    end_time: str, 
    location: str = None,
    description: str = None,
    attendees: list = None) -> str:
    """
    Creates a calendar event in the user's primary calendar.

    Parameters:
    - summary: A short description or title of the event.
    - start_time: The start time in ISO 8601 format (e.g., '2025-07-23T10:00:00+05:30').
    - end_time: The end time in ISO 8601 format.
    - location: (Optional) Location of the event Inoffice or teams/google-meet.
    - description: (Optional) Description or agenda.
    - attendees: (Optional) List of attendee email addresses.

    Returns:
    - The ID of the created event if success or an error message if creation fails.
    """
    try:
        service = get_google_service('calendar', 'v3')
        event = {
            'summary': summary,
            'start': {
                'dateTime': start_time,
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'Asia/Kolkata',
            }
        }
        if location:
            event['location'] = location
        if description:
            event['description'] = description
        if attendees:
            event['attendees'] = [{'email': email} for email in attendees]

        event_result = service.events().insert(calendarId='primary', body=event).execute()
        return f"Event created: {event_result.get('id')}"
    except Exception as e:
        return f"Failed to create event: {str(e)}"

