from .getGmailService import get_gmail_service
import base64
import json

# def fetch_unread_emails(max_results=5):
#     service = get_gmail_service()
#     results = service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD'], maxResults=max_results).execute()
#     messages = results.get('messages', [])
    
#     unread_emails = []

#     for msg in messages:
#         msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
#         headers = msg_data['payload']['headers']
#         subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "(No Subject)")
#         sender = next((h['value'] for h in headers if h['name'] == 'From'), "(Unknown Sender)")

#         try:
#             body = msg_data['payload']['parts'][0]['body']['data']
#         except (KeyError, IndexError):
#             body = msg_data['payload']['body'].get('data', '')
        
#         decoded_body = base64.urlsafe_b64decode(body.encode('ASCII')).decode('utf-8', errors='ignore')
        
#         unread_emails.append({
#             'from': sender,
#             'subject': subject,
#             'body': decoded_body.strip()
#         })

#     return unread_emails


from base64 import urlsafe_b64decode
from googleapiclient.errors import HttpError

def fetch_emails(max_results=10):
    service = get_gmail_service()
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
