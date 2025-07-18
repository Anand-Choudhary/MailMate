from fastapi import FastAPI
from mail.getGmailService import get_gmail_service
from mail.fetchMail import fetch_unread_emails

data = fetch_unread_emails()
print("DATA -> ",data)


app = FastAPI()

