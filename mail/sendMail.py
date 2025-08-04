from langchain_core.tools import tool
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from getGmailService import get_google_service

@tool
def send_mail_tool(to: list, subject: str, body: str) -> str:
    """
    Sends an email to the specified recipient.

    Parameters:
    - to: The recipient's email address.
    - subject: The subject line of the email.
    - body: The main content of the email.

    Returns:
    - A confirmation string or error message after attempting to send the email.
    """
    try:

        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject

        service = get_google_service('gmail', 'v1')

        # service = build('gmail', 'v1', credentials=creds)

        sent_message = service.users().messages().send(
            userId='me',
            body={'raw': message}
        ).execute()

        return f"Email sent successfully! Message ID: {sent_message['id']}"

    except Exception as e:
        return f"Failed to send email: {str(e)}"
