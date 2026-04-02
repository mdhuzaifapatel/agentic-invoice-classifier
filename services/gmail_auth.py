import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from config import GMAIL_SCOPES, GMAIL_OAUTH_FILE, GMAIL_TOKEN_FILE

def get_gmail_credentials():
    creds = None

    if os.path.exists(GMAIL_TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(GMAIL_TOKEN_FILE, GMAIL_SCOPES)
    
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            GMAIL_OAUTH_FILE, GMAIL_SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open(GMAIL_TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return creds
