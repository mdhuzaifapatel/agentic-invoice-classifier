# config.py
import os

APP_NAME = "invoice_app"
USER_ID = "invoice_user"

GCS_BUCKET = "invoice-exception-usecase"

# Paths
GCS_SERVICE_ACCOUNT_FILE = "credentials/service_account.json"
GMAIL_OAUTH_FILE = "credentials/oauth.json"
GMAIL_TOKEN_FILE = "credentials/token.json"

GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")