import base64
from googleapiclient.discovery import build

class GmailService:
    def __init__(self, creds):
        self.service = build("gmail", "v1", credentials=creds)

    def fetch_pdf_attachments(self):
        results = self.service.users().messages().list(
            userId="me", q="has:attachment filename:pdf"
        ).execute()

        pdfs = []

        for msg in results.get("messages", []):
            data = self.service.users().messages().get(
                userId="me", id=msg["id"]
            ).execute()

            for part in data.get("payload", {}).get("parts", []):
                if part.get("filename", "").endswith(".pdf"):
                    att = self.service.users().messages().attachments().get(
                        userId="me",
                        messageId=msg["id"],
                        id=part["body"]["attachmentId"]
                    ).execute()

                    pdfs.append({
                        "filename": part["filename"],
                        "data": base64.urlsafe_b64decode(att["data"])
                    })

        return pdfs