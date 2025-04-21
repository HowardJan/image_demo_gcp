from google.cloud import storage
import os

BUCKET_NAME = os.getenv("BUCKET_NAME")

def upload_to_gcs(file_bytes, filename):
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(filename)
    blob.upload_from_string(file_bytes, content_type='image/jpeg')
    blob.make_public()
    return blob.public_url
