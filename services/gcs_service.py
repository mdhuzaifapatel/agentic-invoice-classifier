from google.cloud import storage
from google.oauth2 import service_account
import uuid
import json

class GCSService:
    def __init__(self, bucket_name, service_account_file):
        creds = service_account.Credentials.from_service_account_file(service_account_file)
        self.client = storage.Client(credentials=creds)
        self.bucket = self.client.bucket(bucket_name)
    
    def upload_file(self, file_bytes, classification, filename):
        path = f"Huzaifa/{classification.lower()}/{uuid.uuid4()}_{filename}"
        blob = self.bucket.blob(path)
        blob.upload_from_string(file_bytes)
        return path
    
    def upload_json(self, data, filename):
        path = f"Huzaifa/extracted_jsons/{uuid.uuid4()}_{filename}.json"
        blob = self.bucket.blob(path)
        blob.upload_from_string(json.dumps(data, indent=2))
        return path