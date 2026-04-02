import os
from fastapi import FastAPI

from config import (
    GCS_BUCKET,
    GCS_SERVICE_ACCOUNT_FILE,
    GOOGLE_API_KEY
)

from services.gmail_auth import get_gmail_credentials
from services.gmail_service import GmailService
from services.gcs_service import GCSService
from workflows.pipeline import Pipeline

app = FastAPI()

gcs = GCSService(GCS_BUCKET, GCS_SERVICE_ACCOUNT_FILE)
pipeline = Pipeline(gcs)

@app.get("/")
async def run():
    gmail = GmailService(get_gmail_credentials())
    pdfs = gmail.fetch_pdf_attachments()

    results = []
    for pdf in pdfs:
        results.append(await pipeline.process_pdf(pdf))

    return {"results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="localhost", port=9000, reload=True)
