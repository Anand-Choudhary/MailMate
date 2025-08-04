from getGmailService import get_google_service
import base64
import json


from base64 import urlsafe_b64decode
from googleapiclient.errors import HttpError

def fetch_emails(max_results=10):
    service = get_google_service('gmail', 'v1')
    results = service.users().messages().list(userId='me', labelIds=['UNREAD'], maxResults=max_results).execute()
    messages = results.get('messages', [])

    emails = []
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        payload = msg_data['payload']
        headers = {h['name']: h['value'] for h in payload.get('headers', [])}
        subject = headers.get('Subject', '(No Subject)')
        sender = headers.get('From', '(No Sender)')
        body = get_body(payload)
        emails.append({'id': msg['id'], 'subject': subject, 'sender': sender, 'body': body})

        service.users().messages().modify(
            userId='me',
            id=msg['id'],
            body={'removeLabelIds': ['UNREAD']}
        ).execute()

    return emails

def get_body(payload):
    parts = payload.get('parts', [])
    if not parts:
        return payload.get('body', {}).get('data', '')
    for part in parts:
        if part['mimeType'] == 'text/plain':
            data = part['body'].get('data', '')
            return urlsafe_b64decode(data).decode('utf-8')
    return ''
